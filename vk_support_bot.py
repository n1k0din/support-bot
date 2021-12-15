import vk_api
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

if __name__ == '__main__':
    env = Env()
    env.read_env()

    vk_token = env('VK_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)