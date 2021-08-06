import random
from flask import Flask, request, render_template

app = Flask("__name__", template_folder="template")


@app.route('/', methods=["GET"])
def get_numbers_form():
    return render_template("Lotto.html")


@app.route('/', methods=["POST"])
def post_numbers_form():
    numbers = request.form.getlist("number")
    draws = request.form['draws']
    if validate_numbers(numbers) == True:
        message = draw(int(draws), [int(i) for i in numbers])
    else:
        message = f'wybrales nastepujace liczby: {numbers} Liczba losowan: {draws}' + '          ' + validate_numbers(
            numbers)
    return render_template("Lotto.html", message=message, text=message.split('\n'))


def type_numbers():
    numbers = []
    while len(numbers) != 6:
        try:
            number = int(input(f"type a number {len(numbers) + 1}: "))
            if number not in numbers and number not in range(1, 49):
                print("Number out of range! Select number from 1 to 49")
            elif number not in numbers:
                numbers.append(number)
            else:
                print("you selected this number already. Choose another one")
        except ValueError:
            print("it's not a number!")
    numbers.sort()
    return numbers


def validate_numbers(numbers):
    if len(numbers) != 6:
        return f"You selected {len(numbers)} numbers instead of 6!"
    else:
        return True


def computer_numbers():
    list_ = [n for n in range(1, 49)]
    chosen_numbers = []
    for _ in range(6):
        random_number = random.choice(list_)
        chosen_numbers.append(random_number)
        list_.remove(random_number)

    return chosen_numbers


def draw(number_of_draws=1, user_list=[1, 2, 3, 4, 5, 6]):
    occurrences = {'one': 0, 'two': 0, 'three': 0, 'four': 0, "five": 0, "six": 0}
    # user_list = type_numbers()
    text = ''
    counter = 0
    while counter != number_of_draws:
        computer_list = computer_numbers()
        matches = 0
        for n in user_list:
            if n in computer_list:
                matches += 1
        counter += 1
        if matches == 1:
            occurrences['one'] = occurrences['one'] + 1
        elif matches == 2:
            occurrences['two'] = occurrences['two'] + 1
        elif matches == 3:
            occurrences['three'] = occurrences['three'] + 1
        elif matches == 4:
            occurrences['four'] = occurrences['four'] + 1
        elif matches == 5:
            occurrences['five'] = occurrences['five'] + 1
        elif matches == 6:
            occurrences['six'] = occurrences['six'] + 1

        text += f'you matched {matches} numbers {user_list}         versus {computer_list} \n'
    text += f'\n summary of {number_of_draws} draws: {occurrences}'
    print(text)
    return text


if __name__ == '__main__':
    app.run(debug=True)
