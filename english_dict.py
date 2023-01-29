import random

#Opening the base txt file containing words and meanings and creating a list for random words posting:
f = open("formatted_eng_words.txt", 'r', encoding='UTF-8')
rare_words = f.read().split('\n')
f.close()

#Creating a dictionary for the quiz functionality:
eng_dict = {}
for i in rare_words:
    first_word = i.split()[0]
    eng_dict[first_word] = i.split(maxsplit=1)[1]
keys = list(eng_dict)

#Removing "-" and spaces from values to make it look tidy:
for n in keys:
    eng_dict[n] = eng_dict[n][1:]
    if eng_dict[n][0] == " ":
        eng_dict[n] = eng_dict[n][1:]
    if eng_dict[n][0].isupper():
        eng_dict[n] = eng_dict[n][0].lower() + eng_dict[n][1:]
#End of Dict Creating.
#Now we have "rare_words" list for random word-meaning bot replies AND a separate {word : meaning} dictionary for the quiz.


def random_word():
    return random.choice(rare_words)


def quiz_attempt():
    quiz_list = []
    for i in range(4):
        x = random.choice(keys)
        quiz_list.append(x)
        #del dictionary[x]
        #keys.remove(x)
    return quiz_list

