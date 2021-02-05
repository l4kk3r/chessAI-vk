import vk_api
import random
import main2
from vk_api.longpoll import VkLongPoll, VkEventType


# API-ключ созданный ранее
token = "9c22d96c2151feb2fb044674b411b190a38cab1ae2e4eef6d47e885f2cb69ac027b2e2d381d1ad248ac8f"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)
api = vk.get_api()
# Работа с сообщениями
longpoll = VkLongPoll(vk)
print("working!")
status = {}
# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:

            # Сообщение от пользователя
            request = event.text
            if event.user_id in status and status[event.user_id] == 'playing':
                if request.lower() == 'stop':
                    status[event.user_id] = 'waiting'
                    api.messages.send(user_id=event.user_id, message='Бот остановлен!',
                                      random_id=random.randint(-9999999999, 999999999))
                else:
                    main2.make_move(api, event.user_id, request)
            else:
                if request == 'start':
                    main2.start_ai()
                    status[event.user_id] = 'playing'
                    api.messages.send(user_id=event.user_id, message='Бот запущен! Ожидаем хода',
                                      random_id=random.randint(-9999999999, 999999999))
                # Каменная логика ответа
                else:
                    api.messages.send(user_id=event.user_id, message=request,
                                      random_id=random.randint(-9999999999, 999999999))