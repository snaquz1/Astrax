import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from Users.models import CustomUser
from Chat.models import *


# Create your views here.

PHOTO_EXTENSIONS = ['jpg', 'jpeg', 'gif', 'png', 'webp']
VIDEO_EXTENSIONS = ['mp4']
GIF_EXTENSIONS = ['gif']

def serialize_attachment(att):
    ext = (att.extension or "").lower()
    return {
        "id": att.id,
        "url": att.file.url,
        "extension": ext,
        "is_image": ext in PHOTO_EXTENSIONS,
        "is_video": ext in VIDEO_EXTENSIONS,
        "is_gif": ext in GIF_EXTENSIONS,
    }

@login_required
@require_POST
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    user = request.user
    if not ChatMember.objects.filter(user=user, chat=chat).exists():
        return JsonResponse({"error": "You are not a member of this chat."}, status=403)
    text = request.POST.get('text', "")
    files = request.FILES.getlist('files')
    if not text and not files:
        return JsonResponse({"error": "You need to send at least one file."}, status=400)
    message = Message.objects.create(
        chat=chat,
        username=user.username,
        text=text,
    )

    attachments_data = []

    for f in files:
        _, ext = os.path.splitext(f.name)
        ext = ext.lower().lstrip(".")
        attachment = Attachment.objects.create(
            message=message,
            file=f,
            ext=ext,
        )
        attachments_data.append(serialize_attachment(attachment))

        event_data = {
            "type": "chat.message",
            "message_id": message.id,
            "chat_id": chat.id,
            "message": message.text,
            "username": user.username,
            "attachments": attachments_data,
            "created_at": message.created_at.isoformat(),
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.id}",
            event_data
        )

        return JsonResponse({
            "success": True,
            "data": event_data
        })




@login_required
def index(request):
    members = None
    messages = None
    selected_chat = None
    user_role = None
    openmodal = None
    get_openmodal = request.session.get("openmodal")
    if get_openmodal == True:
        openmodal = True
        request.session["openmodal"] = False
    selected_chat_id = request.GET.get("chat_id")
    chats = Chat.objects.filter(members__username__contains=request.user)
    if selected_chat_id:
        selected_chat = get_object_or_404(Chat, id=selected_chat_id)
        if request.user not in selected_chat.members.all():
            return redirect("error")
        messages = Message.objects.filter(chat=selected_chat)
        messages = messages.prefetch_related("attachment_set")
        messages = messages.select_related("username")
        members = ChatMember.objects.filter(chat=selected_chat).select_related("user")
        user_role = members.get(user=request.user).role
    return render(request, 'index.html', {'chats': chats, "messages": messages, "selected_chat": selected_chat, "members": members, "user_role": user_role, "openmodal": openmodal})

@login_required
def create_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    title = request.POST.get("title")
    if title:
        chat = Chat.objects.create(title=request.POST.get("title"))
        ChatMember.objects.create(chat=chat, user=request.user, role="admin")

        return redirect("/")
    return JsonResponse({"error": "title cannot be Empty"}, status=405)

def invite(request, token):
    chat = get_object_or_404(Chat, invite_token=token)
    if request.user in chat.members.all():
        return redirect(f"/?chat_id={chat.id}")
    if chat:
        ChatMember.objects.create(chat=chat, user=request.user)
        Message.objects.create(chat=chat, username=request.user, text=f"{request.user} присоеденился к чату")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.id}",
            {
                "type": "chat_message",
                "message": f"{request.user} присоеденился к чату",
                "username": request.user.username
            }
        )
        return redirect(f"/?chat_id={chat.id}")
    return HttpResponse(status=404)

@login_required
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    member = ChatMember.objects.get(chat=chat, user=request.user)
    if member.role == "admin":
        chat.delete()
        return redirect("/")

    return redirect("error")

def manage_user(request, member_id, chat_id, operation):
    if operation == "delete":
        chat = get_object_or_404(Chat, id=chat_id)
        members = ChatMember.objects.filter(chat=chat).select_related("user")
        user_role = members.get(user=request.user).role
        if user_role == "admin":
            kicked_user = get_object_or_404(ChatMember, chat=chat, id=member_id)
            channel_layer = get_channel_layer()
            #дисконнектим от канала
            async_to_sync(channel_layer.group_send)(
                f"user_{kicked_user.user.id}",
                {
                    "type": "force_disconnect",
                    "chat_id": chat_id
                }
            )
            kicked_user.delete()
            kicked_text = f"Пользователь {kicked_user.user.username} был удален пользователем {request.user.username}({user_role})"
            Message.objects.create(chat=chat, username=request.user, text=kicked_text)
            request.session["openmodal"] = True
            return redirect(f"/?chat_id={chat_id}")
        return redirect("error")


def updatemodal(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    members = chat.members.all()

    return render(request, 'partials/modal.html',
                  {"chat": chat, "members": members})



def error(request):
    return render(request, "error404.html")