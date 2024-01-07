import random
import string

def _generate_unicode_characters(n):
    return ''.join(random.choice(string.punctuation) for _ in range(n))

def _add_arbitrary_trailing_spaces(sentence):
    initial_spaces = random.randint(0, 5)
    final_spaces = random.randint(0, 5)
    return " " * initial_spaces + sentence + " " * final_spaces

_target = [
    "The black cat crossed the street with elegance.",
    "Where did you leave the keys to the car?",
    "What a surprise to see you here!",
    "I would like to ask you a very important favor.",
    "Sometimes, things are not what they seem.",
    "Patience is key to success.",
    "Don't worry, everything will be fine!",
    "It's never too late to learn something new.",
    "Life is like a roller coaster; it has its ups and downs.",
    "You can't always win, but you can always learn.",
    "What is your all-time favorite movie?",
    "Watch out for the dog!",
    "Change is the only constant in life.",
    "Have you ever tried German food?",
    "The truth always finds the light.",
    "Sometimes, it's better to be alone than in bad company.",
    "Life is a puzzle; find the pieces that fit with you.",
    "What do you think of the current politics in your country?",
    "Laughter is the best medicine.",
    "Today is a good day to smile!",
    "Do you have any superstitions?",
    "Trust is earned drop by drop, but lost in one blow.",
    "How was your week at work?",
    "The art of simplicity is a complicated task.",
    "I hope you have a wonderful day.",
    "Congratulations on your achievement!",
    "Curiosity killed the cat, but satisfaction brought it back.",
    "I would love to learn German someday.",
    "Sometimes, you need to get lost to find yourself.",
    "You can't always have everything.",
    "Do you like spicy food?",
    "What is your greatest achievement so far in life?",
    "Life is too short to worry about insignificant things.",
    "Can you cook German dishes?",
    "Sometimes, it's good not to have a plan.",
    "What would you do if you won the lottery tomorrow?",
    "Do you have any long-term goals?",
    "Life is like a cup of tea; it all depends on how you brew it.",
    "How was your day?",
    "Not all who wander are lost.",
    "I love your sense of humor.",
    "Hope is the dream of the awake.",
    "What a beautiful day today!",
    "What does success mean to you?",
    "It's never too late to change direction.",
    "Life is like a box of chocolates; you never know what you're gonna get.",
    "Can I ask you for advice?",
    "Every cloud has a silver lining.",
    "Do you have any pets?",
    "Beauty is in the eye of the beholder.",
    "You can't always control what happens to you, but you can always control how you react.",
    "How many languages do you speak?",
    "Never judge a book by its cover.",
    "Can you give me some advice?",
    "It's not always easy to make decisions.",
    "Life is like a ten-speed bicycle; most of us have gears we never use.",
    "Prevention is better than cure.",
    "Do you have any short-term goals?",
    "All that glitters is not gold.",
    "Have you ever tried apple strudel?",
    "Life is but a dream.",
    "I can't believe it!",
    "What do you think about the current world situation?",
    "Life is a play that does not allow rehearsals.",
    "Good luck in your new project!",
    "Sometimes, opportunities only come once.",
    "What would you do if you met an alien?",
    "open",
    "close",
    "rich day"
]


def generate_text_sample(as_gen: bool = False):
    return (
            _add_arbitrary_trailing_spaces(sentence) + _generate_unicode_characters(random.randint(0, 4)) 
            for sentence in _target
    ) if as_gen else [
            _add_arbitrary_trailing_spaces(sentence) + _generate_unicode_characters(random.randint(0, 4)) 
            for sentence in _target
    ]