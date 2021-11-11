




import os
import telebot
from telebot import types

from Messages import *
from dataEgine import *


BOT_TOKEN='1908250775:AAFoQFc2_qQbl8VhVxwm9m88nsSwOQVNHyI'
ENV = bool(environ.get('ENV', False))

if ENV:
    BOT_TOKEN = environ.get('BOT_TOKEN', None)
 
else:
    BOT_TOKEN = config.BOT_TOKEN
  







bot = telebot.TeleBot(BOT_TOKEN)


def inline_menu():
    """
    Create inline menu for new chat
    :return: InlineKeyboardMarkup
    """
    callback = types.InlineKeyboardButton(text='\U0001f680" Start The Flight', callback_data='/next')
  

    feedback = types.InlineKeyboardButton(text='\U0001f699 feedback', callback_data='/feedback')
    menu = types.InlineKeyboardMarkup()
    menu.add(callback)
    menu.add(feedback)

    return menu


def generate_markup():
    """
    Create menu with two buttons: 'Like' and 'Dislike'
    :return: ReplyKeyboardMarkup
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    markup.add(like_str)
    markup.add(dislike_str)
    return markup


def connect_user(user_id):
    """
    :param user_id: Chat id with user
    :return: boolean
    """
    if user_id in communications:
        return True
    else:
        bot.send_message(user_id, m_has_not_dialog)
        return False


@bot.message_handler(commands=['start'])
def echo(message):
    """
    Make the user in Data Base.
    :param message:
    :return:
    """
    message.chat.type = 'private'
    user_id = message.chat.id


    if message.chat.username is None:
        bot.send_message(user_id, m_is_not_user_name)
        return

    menu = inline_menu()

    bot.send_message(user_id, m_start, reply_markup=menu)




@bot.message_handler(commands=['next'])
def echo(message):
    """
    for next
    """
    
    message.chat.type = 'private'
    user_id = message.chat.id


    if message.chat.username is None:
        bot.send_message(user_id, m_is_not_user_name)
        return

    menu = inline_menu()
    bot.send_message(user_id,m_start,reply_markup=menu)


@bot.message_handler(commands=['stop'])
def echo(message):
    """
    This function remove user from Data Base and sends a farewell message.
    :param message:
    :return:
    """
    menu = types.ReplyKeyboardRemove()
    user_id = message.chat.id

    if message.chat.id in communications:

        bot.send_message(communications[user_id]['UserTo'], m_disconnect_user, reply_markup=menu)

        tmp_id = communications[user_id]['UserTo']
        delete_info(tmp_id)

    delete_user_from_db(user_id)

    bot.send_message(user_id, m_good_bye)









@bot.message_handler(func=lambda call: call.text == like_str or call.text == dislike_str)
def echo(message):
    """
    This function reacts to pressing buttons: 'Like' and 'Dislike'
    If both users press 'Like', then bot sends them username from telegram.
    If somebody press 'Dislike', then chat finish.
    :param message:
    :return:
    """
    user_id = message.chat.id

    if user_id not in communications:
        bot.send_message(user_id, m_failed, reply_markup=types.ReplyKeyboardRemove())
        return

    user_to_id = communications[user_id]['UserTo']

    flag = False

    if message.text == dislike_str:
        bot.send_message(user_id, m_dislike_user, reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(user_to_id, m_dislike_user_to, reply_markup=types.ReplyKeyboardRemove())
        flag = True
    else:
        bot.send_message(user_id, m_like)#reply_markup=types.ReplyKeyboardRemove())

        #update_user_like(user_to_id)

        if communications[user_id]['like'] == communications[user_to_id]['like']:
            bot.send_message(user_id, m_all_like(communications[user_id]['UserName']))
            bot.send_message(user_to_id, m_all_like(communications[user_to_id]['UserName']))
            flag = True

    if flag:
        delete_info(user_to_id)
        menu = inline_menu()
        bot.send_message(user_id, m_play_again, reply_markup=menu)
        bot.send_message(user_to_id, m_play_again, reply_markup=menu)






     
  


@bot.message_handler(content_types=['text', 'sticker', 'video', 'photo', 'audio', 'voice'])
def echo(message):
  
    """
    Resend message to anonymous friend.
    :param message:
    :return:
    """
    user_id = message.chat.id
    if message.content_type == 'sticker':
        if not connect_user(user_id):
            return

        bot.send_sticker(communications[user_id]['UserTo'], message.sticker.file_id)



    elif  message.content_type == 'photo':
      bot.send_message(communications[user_id]['UserTo'],photo_user_msg)
      bot.send_message(user_id, photo_partner_msg)
       
      
      if not connect_user(user_id):
            return

      file_id = None

      for item in message.photo:
            file_id = item.file_id

      bot.send_photo(communications[user_id]['UserTo'], file_id, caption=message.caption)
   
    elif message.content_type == 'audio':
        if not connect_user(user_id):
            return

        bot.send_audio(communications[user_id]['UserTo'], message.audio.file_id, caption=message.caption)
    elif message.content_type == 'video':
        if not connect_user(user_id):
            return

        bot.send_video(communications[user_id]['UserTo'], message.video.file_id, caption=message.caption)
    elif message.content_type == 'voice':
        if not connect_user(user_id):
            return

        bot.send_voice(communications[user_id]['UserTo'], message.voice.file_id)
    elif message.content_type == 'text':
      filter_wrongs=["horny","sexy","bad","naughty","sange","sex","dick","pussy","sangap","suck","fuck","middle finger","18+","🖕","👉","👅","💋","💦","🍑","🍆","👙","🍒","🌮","cum","insideme","ass","kiss","sperm","suck","fucking","sucking","licking","tongue","wet","undress","naked","fingering","fapchat","sexter","ruh","dum","faxting"]
      s=message.text.split(' ')
      flag=False
      for i in s:
        for j in filter_wrongs:
          if i==j:
      
            flag=True
            break
      if flag==True:
        print("partner is violating ")
        bot.send_message(communications[user_id]['UserTo'],violation_user_msg)
        bot.send_message(user_id, violation_partner_msg)
       
      else:

   

        if message.text != '/start' and message.text != '/stop' and \
                    message.text != dislike_str and message.text != like_str and message.text != '/next':





            if not connect_user(user_id):
                return

            if message.reply_to_message is None:
                bot.send_message(communications[user_id]['UserTo'], message.text)
            elif message.from_user.id != message.reply_to_message.from_user.id:
                bot.send_message(communications[user_id]['UserTo'], message.text,
                                 reply_to_message_id=message.reply_to_message.message_id - 1)
            else:
                bot.send_message(user_id, m_send_some_messages)


@bot.message_handler(commands=['sharelink'])
def echo(message):
   if message.chat.id in communications:
       user_id = message.chat.id
       user_to_id = communications[user_id]['UserTo']

      # bot.send_message(communications[user_id]['UserTo'],violation_user_msg['UserName'])
      # bot.send_message(user_id, violation_partner_msg['UserName'])
       bot.send_message(user_id, m_all_like(communications[user_to_id]['UserName']))
   


       bot.send_message(communications[user_id]['UserTo'],error_sharelink_msg)
       bot.send_message(user_id,error_sharelink_msg)
    





   


      
    
    

@bot.callback_query_handler(func=lambda call: True)
def echo(call):
    """
    Create new chat.
    All users are divided into two categories: receivers and emitters.
    If bot finds pair, then it creates new chat.
    :param call:
    :return:
    """
    if call.data == '/next':
        user_id = call.message.chat.id
        user_to_id = None

        add_users(chat=call.message.chat)

        if len(free_users) < 2:
            bot.send_message(user_id, m_is_not_free_users)
            return

        if free_users[user_id]['state'] == 0:
            return

        for user in free_users:
            if user['state'] == 0:
                user_to_id = user['ID']
                break

        if user_to_id is None:
            bot.send_message(user_id, m_is_not_free_users)
            return

        keyboard = generate_markup()

        add_communications(user_id, user_to_id)

        bot.send_message(user_id, m_is_connect, reply_markup=keyboard)
        bot.send_message(user_to_id, m_is_connect, reply_markup=keyboard)


if __name__ == '__main__':
    recovery_data()
    bot.stop_polling()
    bot.polling(none_stop=True)
