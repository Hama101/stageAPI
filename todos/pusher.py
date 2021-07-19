import pusher

pusher_client = pusher.Pusher(
    app_id='1237851',
    key='b7c718dd993da96747a5',
    secret='678b0395186ab6819106',
    cluster='eu',
    ssl=True
)

#pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})