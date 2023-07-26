from colorama import Fore, Back, Style
from settings import colors

#x = 1201
color_x = None


def color_lp_profit(x):
    # Определяет цвет текста, в зависимости от кол-ва выводимого LP.
    if x < 800:
#        print('Меньше 800')
        if colors:
            color_x = f'{Fore.LIGHTRED_EX}{x:,.0f}{Style.RESET_ALL}'
        else:
            color_x = f'{x:,.0f}'
    elif x >= 800 and x < 1000:
#        print('800 - 100')
        if colors:
            color_x = f'{Fore.LIGHTYELLOW_EX}{x:,.0f}{Style.RESET_ALL}'
        else:
            color_x = f'{x:,.0f}'
    elif x >= 1000 and x <= 1200:
#        print('800-1000')
        if colors:
            color_x = f'{Fore.LIGHTGREEN_EX}{x:,.0f}{Style.RESET_ALL}'
        else:
            color_x = f'{x:,.0f}'
    elif x > 1200 and x <= 1400:
#        print('1200+')
        if colors:
            color_x = f'{Fore.GREEN}{x:,.0f}{Style.RESET_ALL}'
        else:
            color_x = f'{x:,.0f}'
    elif x > 1400:
        if colors:
            color_x = f'{Fore.MAGENTA}{x:,.0f}{Style.RESET_ALL}'
        else:
            color_x = f'{x:,.0f}'
    return color_x


#color_lp_profit(x)
