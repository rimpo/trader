import dramatiq

@dramatiq.actor
def process_ticks(ticks):
    print("got tick!!")
    print(ticks)
    pass