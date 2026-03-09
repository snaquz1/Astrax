from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from Users.models import CustomUser
from Chat.models import *


# Create your views here.
@login_required
def ws_demo(request):
    return render(request, "ws_demo.html")

@login_required
def index(request):
    messages = None
    selected_chat = None
    selected_chat_id = request.GET.get("chat_id")
    chats = Chat.objects.filter(members__username__contains=request.user)
    if selected_chat_id:
        selected_chat = get_object_or_404(Chat, id=selected_chat_id)
        messages = Message.objects.filter(chat=selected_chat)
        messages = messages.prefetch_related("attachment_set")
        messages = messages.select_related("username")

    return render(request, 'index.html', {'chats': chats, "messages": messages, "selected_chat": selected_chat})

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
    if chat:
        ChatMember.objects.create(chat=chat, user=request.user)
        Message.objects.create(chat=chat, username=request.user, text="Присоеденился к чату")
        return redirect(f"/?chat_id={chat.id}")
    return HttpResponse(status=404)
@login_required
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.delete()
    return redirect("/")

@login_required
def chat_room(request, chat_id):
    return render(request, "ws_demo.html", {"chat_id": chat_id})