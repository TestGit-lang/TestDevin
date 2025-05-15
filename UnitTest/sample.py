import math

def trial_odd_sqrt(target):
    """
    3以上の整数で割ることができるかを判定する。
    
    Parameters
    ----------
    target : int
        判定したい整数。

    Returns
    -------
    value : bool
        割ることができる場合はTrue、割ることができない場合はFalse。
    """
    i = 3

    root_target = math.sqrt(target)

    while i <= root_target:
        if target % i == 0:
            return False

        i += 2

    return True


def check_prime_number(num):
    """
    素数かどうかを判定する。
    
    Parameters
    ----------
    num : int
        判定したい整数。

    Returns
    -------
    value : bool
        素数の場合はTrue、素数でない場合はFalse。
    """
    if num == 1:
        return False

    elif num == 2:
        return True

    elif num % 2 == 0:
        return False

    else:
        return trial_odd_sqrt(num)

# value = 677043
# print(check_prime_number(value))