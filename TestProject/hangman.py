"""
my new code
"""


def get_Attempts(i):
    num = 5
    str_input = 'Enter number of attempts, between ' + str(i) + ' and 20 - '
    num = int(input(str_input))
    if num < i or num > 20:
        print('{0} is not in the range, using default 5'.format(num))
        return 5
    return num


def get_Word_Len():
    leng = 5
    leng = int(input('Enter the word length, between 4 and 10 - '))
    if leng < 4 or leng > 10:
        print('{0} length is not as expected, using the default 5'.format(leng))
        return 5
    return leng


def checkGameResult(answer, tmp, i):
    print("After {0} attemps".format(i+1))
    print(list(tmp))
    print('================')

    if answer == tmp:
        return True
    else:
        return False


def getRandomWord(leng):
    from random_word import RandomWords
    r = RandomWords()
    return r.get_random_word(minLength=leng, maxLength=leng)


def main():
    import re

    leng = get_Word_Len()
    num = get_Attempts(leng)

    # len = 6
    # num = 6

    print('-------------')
    print('total attempts given {0}'.format(num))
    print('word length for this game{0}'.format(leng))
    print('enjoy the game !!!')
    print('-------------')

    test_Word = getRandomWord(leng)
    test_Word = test_Word.upper()
    # print(test_Word)
    tList = [' '] * leng

    for i in range(num):
        print("Try ", format(i+1))
        letter = input('Enter the alphabet - ').upper()

        try:
            test_Word.index(letter)
        except ValueError:
            pass
        else:
            for elem in re.finditer(letter, test_Word):
                tList[elem.start()] = letter

        final_ans = ''.join(tList)
        result = checkGameResult(test_Word, final_ans, i)
        if result:
            break
        else:
            pass

    if not result:
        print('better luck next time')
        print('You could not guess it correctly this time')
        print('Actual word was  - ', test_Word)
        print('You guessed      - ', final_ans)
    else:
        print('Congratulation !!!!')
        print('You won in {0} attempts'.format(i+1))
        print('You guessed      - ', final_ans)


if __name__ == "__main__":
    main()
