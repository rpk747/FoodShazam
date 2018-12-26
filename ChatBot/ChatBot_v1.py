
import requests
import datetime
import telebot


#======================================
class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=100):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        #print(resp.json());
        result_json = resp.json()['result']
        #print(result_json);
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_photo(self, chat_id, photo):

        params = {'chat_id': chat_id,'photo': open('D:\Project\Multimodal\pizza.jpg', 'rb')}
        files = {'file': open('D:\Project\Multimodal\pizza.jpg', 'rb')}
        method = 'sendPhoto'
        print("IN")
        resp = requests.post(self.api_url + method, files=files)
        print(resp.status_code, resp.reason, resp.content)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        #print(last_update);
        return last_update

#======================================
State = type("State",(object,),{})

class Start(State):
    def Execute(self,Foodbot,last_chat_text,last_chat_id,last_chat_name):
        if last_chat_text == '/start':
            food_bot.send_message(last_chat_id,'Welcome to Food Shazam, your cooking assistant. Please start with a greeting. Thank you')
            Foodbot.FSM.SetState("Greetings")
        else:
            food_bot.send_message(last_chat_id,'Please start the application with "/start", {}'.format(last_chat_name))

class Greetings(State):

    def Execute(self,Foodbot,last_chat_text,last_chat_id,last_chat_name):
        now = datetime.datetime.now()
        today = now.day
        hour = now.hour

        if last_chat_text.lower() in greetings and today == now.day and 0 <= hour < 12:
            food_bot.send_message(last_chat_id, 'Good Morning {}'.format(last_chat_name))
            food_bot.send_message(last_chat_id, 'Hope you are doing great this morning :)')
            Foodbot.FSM.SetState("getIngredients")
            Foodbot.FSM.Execute(Foodbot, last_chat_text, last_chat_id, last_chat_name)

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            food_bot.send_message(last_chat_id, 'Good Afternoon {}'.format(last_chat_name))
            food_bot.send_message(last_chat_id, 'Hope you are doing great this afternoon :)')
            Foodbot.FSM.SetState("getIngredients")
            Foodbot.FSM.Execute(Foodbot, last_chat_text, last_chat_id, last_chat_name)

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            food_bot.send_message(last_chat_id, 'Good Evening {}'.format(last_chat_name))
            food_bot.send_message(last_chat_id, 'Hope you are doing great this evening :)')
            Foodbot.FSM.SetState("getIngredients")
            Foodbot.FSM.Execute(Foodbot, last_chat_text, last_chat_id, last_chat_name)

        elif last_chat_text.lower() not in greetings:
            food_bot.send_message(last_chat_id, 'Wrong Message {}. Please use another greeting!'.format(last_chat_name))
        #print(Foodbot.FSM.curState)

class getIngredients(State):

    def Execute(self,Foodbot,last_chat_text,last_chat_id,last_chat_name):
       # if init_flag and last_chat_text != '/start' and err == False:
        food_bot.send_message(last_chat_id, 'What are the ingredients available with you?')
        food_bot.send_message(last_chat_id, 'Note : Type the available ingredients with comma after each.'.format(last_chat_name))

        #food_bot.send_photo(last_chat_id, 'D:\Project\Multimodal\pizza.jpg')
        Foodbot.FSM.SetState("resIngredients")
        #Foodbot.FSM.Execute(Foodbot, last_chat_text, last_chat_id, last_chat_name)
        init_flag = False
        return

class resIngredients(State):
    def Execute(self,Foodbot,last_chat_text,last_chat_id,last_chat_name):
        ingredients_list = last_chat_text.split(",");
        # ingredients_list.append(last_chat_text);
        # print(json.dumps(last_chat_text));
        print(ingredients_list)
        food_bot.send_message(last_chat_id, 'The ingredients available with you are: {}'.format(ingredients_list))
        food_bot.send_message(last_chat_id, 'Confirm? (Yes or No)')
        Foodbot.FSM.SetState("asktypeofdish")

class asktypeofdish(State):
    def Execute(self,Foodbot,last_chat_text,last_chat_id,last_chat_name):
        if last_chat_text == 'Yes':
            food_bot.send_message(last_chat_id, 'What kind of dish you have in mind- Appetizer, Main Courses, Desserts?')
            Foodbot.FSM.SetState("gettypeofdish")
        elif last_chat_text == 'No':
            food_bot.send_message(last_chat_id, 'Why dont you try again :)')
            Foodbot.FSM.SetState("getIngredients")
        else:
            food_bot.send_message(last_chat_id, 'Sorry {},I dont understand your response, Why dont you try again :) '.format(last_chat_name))
            Foodbot.FSM.SetState("getIngredients")
        return

class gettypeofdish(State):
    def Execute(self, Foodbot, last_chat_text, last_chat_id, last_chat_name):
        print(last_chat_text)
        typofDish = last_chat_text;
        if last_chat_text.lower() not in dishes:
            food_bot.send_message(last_chat_id, 'Sorry {}, I dont understand this type of dish - {}'.format(last_chat_name,last_chat_text))
            food_bot.send_message(last_chat_id, 'Wanna try again? (Yes or No)')
            Foodbot.FSM.SetState("asktypeofdish")
        else:
           food_bot.send_message(last_chat_id, 'Type of dish requested is: {}'.format(typofDish))
           food_bot.send_message(last_chat_id, 'Confirm? (Yes or No)')
           Foodbot.FSM.SetState("askprefTime")
        # Foodbot.FSM.Execute(Foodbot, last_chat_text, last_chat_id, last_chat_name)
        init_flag = False
        return


class askprefTime(State):
    def Execute(self,Foodbot,last_chat_text,last_chat_id,last_chat_name):
        if last_chat_text == 'Yes':
            food_bot.send_message(last_chat_id, 'do you have enough time to cook (Yes or No)? :D')
            Foodbot.FSM.SetState("getprefTime")
        elif last_chat_text == 'No':
            food_bot.send_message(last_chat_id, 'Why dont you try again :)')
            Foodbot.FSM.SetState("asktypeofdish")
        else:
            food_bot.send_message(last_chat_id, 'Sorry {},I dont understand your response, Why dont you try again :) '.format(last_chat_name))
            Foodbot.FSM.SetState("asktypeofdish")
        return

class getprefTime(State):
    def Execute(self, Foodbot, last_chat_text, last_chat_id, last_chat_name):
        print(last_chat_text)
        prefTimeLong = last_chat_text;
        if last_chat_text == 'Yes':
            food_bot.send_message(last_chat_id, 'I have just the thing for you :)')
            food_bot.send_message(last_chat_id, 'Processing.....')
        elif last_chat_text == 'No':
           food_bot.send_message(last_chat_id, 'Lol ,I have just the thing for you :D ')
           food_bot.send_message(last_chat_id, 'Processing.....')
        # Foodbot.FSM.Execute(Foodbot, last_chat_text, last_chat_id, last_chat_name)
        init_flag = False
        return
#======================================

class Transition(object):
    def __init__(self,toState):
        self.toState = toState
        #print(self.toState)

    def Execute(self):
        print("Transitioning")
#======================================

class SimpleFSM(object):
    def __init__(self,char):
        self.char = char
        self.states = {}
        self.transitions = {}
        self.curState = None
        self.trans = None

    def SetState(self,stateName):
        self.curState = self.states[stateName]

    def Transition(self,transName):
        self.trans = self.transitions[transName]
        #print(transName)

    def Execute(self,Foodbot,last_chat_text,last_chat_id,last_chat_name):
        if(self.trans):
            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.trans = None
        self.curState.Execute(Foodbot,last_chat_text,last_chat_id,last_chat_name)
#======================================

class Char(object):
    def __init__(self):
        self.FSM =SimpleFSM(self)
        self.LightOn = True

#======================================


food_bot = BotHandler("697499453:AAFutaF8HeQ1PB2oHhtRZYd4cBa03RHgREY")
greetings = ('hello', 'hi', 'greetings', 'sup', 'hey')
dishes = ('appetizer', 'main courses', 'desserts', 'soup', 'lunch')

def main():
    new_offset = None

    Foodbot = Char()

    Foodbot.FSM.states["Start"] = Start()
    Foodbot.FSM.states["Greetings"] = Greetings()
    Foodbot.FSM.states["getIngredients"] = getIngredients()
    Foodbot.FSM.states["resIngredients"] = resIngredients()
    Foodbot.FSM.states["asktypeofdish"] = asktypeofdish()
    Foodbot.FSM.states["gettypeofdish"] = gettypeofdish()
    Foodbot.FSM.states["askprefTime"] = askprefTime()
    Foodbot.FSM.states["getprefTime"] = getprefTime()


    #print(Foodbot.FSM.states)
    Foodbot.FSM.transitions["toStart"] = Transition("Start")
    Foodbot.FSM.transitions["toGreetings"] = Transition("Greetings")
    Foodbot.FSM.transitions["togetIngredients"] = Transition("getIngredients")
    Foodbot.FSM.transitions["toresIngredients"] = Transition("resIngredients")
    Foodbot.FSM.transitions["toasktypeofdish"] = Transition("asktypeofdish")
    Foodbot.FSM.transitions["togettypeofdish"] = Transition("gettypeofdish")
    Foodbot.FSM.transitions["toaskprefTime"] = Transition("askprefTime")
    Foodbot.FSM.transitions["togetprefTime"] = Transition("getprefTime")

    Foodbot.FSM.SetState("Start")
    print(Foodbot.FSM.curState)
    while True:
            food_bot.get_updates(new_offset)
            last_update = food_bot.get_last_update()

            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']

            #print(Foodbot.FSM.curState)

            if Foodbot.FSM.curState == Foodbot.FSM.states["Start"]:
                Foodbot.FSM.Transition("toStart")
            elif Foodbot.FSM.curState == Foodbot.FSM.states["Greetings"]:
                Foodbot.FSM.Transition("toGreetings")
            elif Foodbot.FSM.curState == Foodbot.FSM.states["getIngredients"]:
                Foodbot.FSM.Transition("togetIngredients")
            elif Foodbot.FSM.curState == Foodbot.FSM.states["resIngredients"]:
                Foodbot.FSM.Transition("toresIngredients")
            elif Foodbot.FSM.curState == Foodbot.FSM.states["asktypeofdish"]:
                Foodbot.FSM.Transition("toasktypeofdish")
            elif Foodbot.FSM.curState == Foodbot.FSM.states["gettypeofdish"]:
                Foodbot.FSM.Transition("togettypeofdish")
            elif Foodbot.FSM.curState == Foodbot.FSM.states["askprefTime"]:
                Foodbot.FSM.Transition("toaskprefTime")
            elif Foodbot.FSM.curState == Foodbot.FSM.states["getprefTime"]:
                Foodbot.FSM.Transition("togetprefTime")

            Foodbot.FSM.Execute(Foodbot,last_chat_text,last_chat_id,last_chat_name)
            new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

