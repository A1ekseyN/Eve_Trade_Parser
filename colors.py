from colorama import Fore, Back, Style


#x = 1201
color_x = None


def color_lp_profit(x):
    # Определяет цвет текста, в зависимости от кол-ва выводимого LP.
    if x < 800:
#        print('Меньше 800')
        color_x = f'{Fore.LIGHTRED_EX}{x:,.0f}{Style.RESET_ALL}'
    elif x >= 800 and x < 1000:
#        print('800 - 100')
        color_x = f'{Fore.LIGHTYELLOW_EX}{x:,.0f}{Style.RESET_ALL}'
    elif x >= 1000 and x <= 1200:
#        print('800-1000')
        color_x = f'{Fore.LIGHTGREEN_EX}{x:,.0f}{Style.RESET_ALL}'
    elif x > 1200 and x <= 1400:
#        print('1200+')
        color_x = f'{Fore.GREEN}{x:,.0f}{Style.RESET_ALL}'
    elif x > 1400:
        color_x = f'{Fore.MAGENTA}{x:,.0f}{Style.RESET_ALL}'
    return color_x


#color_lp_profit(x)
