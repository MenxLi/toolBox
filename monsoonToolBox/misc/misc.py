import typing

def divideChunks(lis: typing.Iterable, n_size: int) -> typing.Iterator:
    for i in range(0, len(lis), n_size): 
        yield lis[i:i + n_size]
