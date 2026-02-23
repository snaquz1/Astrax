from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import title
from pyexpat.errors import messages

from .models import *
# Create your views here.
@login_required
def index(request):
    messages = None
    selected_chat = None
    selected_chat_id = request.GET.get("chat_id")
    chats = Chat.objects.all()
    if selected_chat_id:
        selected_chat = get_object_or_404(Chat, id=selected_chat_id)
        messages = Message.objects.filter(chat=selected_chat)
        messages = messages.prefetch_related("attachment_set")

    return render(request, 'index.html', {'chats': chats, "messages": messages, "selected_chat": selected_chat})
@login_required
def send(request, chat_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    chat = get_object_or_404(Chat, id=chat_id)

    text = (request.POST.get("text") or "").strip()
    files = request.FILES.getlist("files")

    if not text and not files:
        return JsonResponse({"error": "Text or file is required"}, status=400)

    msg = Message.objects.create(chat=chat, text=text)

    if files:
        for file in files:
            Attachment.objects.create(message=msg, file=file)


    return render(request, "partials/message.html", {"msg": msg})
@login_required
def poll(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    after = request.GET.get("after", "0")
    try:
        after_id = int(after)
    except ValueError:
        after_id = 0

    new_messages = (
        Message.objects
        .filter(chat=chat, id__gt=after_id)
        .prefetch_related("attachment_set")
        .order_by("id")
    )

    # Если новых нет — вернем пусто (HTMX ничего не добавит)
    if not new_messages.exists():
        return HttpResponse("")

    return render(request, "partials/messages_batch.html", {"messages": new_messages})
@login_required
def create_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    title = request.POST.get("title")
    if title:
        new_chat = Chat.objects.create(title=request.POST.get("title"))
        return redirect("/")
    return JsonResponse({"error": "title cannot be Empty"}, status=405)







