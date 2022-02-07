
def reformat(events, vacation = False):
    reforatted = []
    if vacation:
        for event in events:
            event_sub_arr = {}
            event_sub_arr['name'] = event.name
            event_sub_arr['start'] = event.start.strftime("%Y-%m-%d %H:%M:%S")
            event_sub_arr['end'] = event.end.strftime("%Y-%m-%d %H:%M:%S")
            event_sub_arr['id'] = event.status if int(event.status) > 0 else '0'
            event_sub_arr['color'] = event.color
            reforatted.append(event_sub_arr)
    else:
        for event in events:
            event_sub_arr = {}
            event_sub_arr['name'] = event.name
            event_sub_arr['start'] = event.start.strftime("%Y-%m-%d %H:%M:%S")
            event_sub_arr['end'] = event.end.strftime("%Y-%m-%d %H:%M:%S")
            event_sub_arr['id'] = event.config.id
            event_sub_arr['color'] = event.config.color
            reforatted.append(event_sub_arr)
    return reforatted

