#!/usr/bin/python

def nextbus(where = 'guess', nbus = 5, walking_time = 3):
    """
    tells you when the next bus is from home or to uni

    where: 'h'/'u'/'guess': home, uni, or try to guess based on wifi connection name
    walking_time: don't show buses less than n mins from now
    nbus: show next n buses

    Example use:
    ~$ bus.py

    ================================
    Current time: 00:58:27    (w=3)
    --------------------------------
       Blumenstr. ---> University
    --------------------------------
    Time   Bus    Arr.   Dur.     In
    --------------------------------
    04:46  102   04:57  00:11  03:48
    05:16  102   05:27  00:11  04:18
    05:35  101*  05:45  00:10  04:37
    05:57  102   06:09  00:12  04:59
    06:11  101*  06:21  00:10  05:13

    * Dudweilerstr. bus stop
    ================================
    
    """

    # guessing requires `wireless`
    # pip install wireless

    def guesser():
        """guess 'u' or 'h'"""
        try:
            from wireless import Wireless
            wireless = Wireless()
            connection = wireless.current()
            if connection.startswith('eduroam') or connection.startswith('saar'):
                return 'u'
            else:
                return 'h'
        except:
            return 'u'

    if where == 'guess':
        where = guesser()

    walking_time = int(walking_time)
    
    # get current time
    import datetime
    now = datetime.datetime.now().time()
    import calendar
    my_date = datetime.datetime.now().today()
    day = calendar.day_name[my_date.weekday()]
    
    if day.lower() == 'sunday' or day.lower() == 'saturday':
        print "\nToday's %s ... stay home!\n" % day
        return

    if where.lower() == 'h':
        # hour, minute, bus number, arrives, duration
        tms = [ ( 4, 46, '102', '04:57', '00:11'),
        ( 5, 16, '102', '05:27', '00:11'),
        ( 5, 35, '101', '05:45', '00:10'),
        ( 5, 57, '102', '06:09', '00:12'),
        ( 6, 11, '101', '06:21', '00:10'),
        ( 6, 20, '124', '06:30', '00:10'),
        ( 6, 26, '150', '06:35', '00:09'),
        ( 6, 27, '102', '06:39', '00:12'),
        ( 6, 41, '101', '06:51', '00:10'),
        ( 6, 43, '109', '06:55', '00:12'),
        ( 6, 50, '124', '07:00', '00:10'),
        ( 6, 52, '150', '07:01', '00:09'),
        ( 6, 57, '102', '07:09', '00:12'),
        ( 7,  5, '124', '07:15', '00:10'),
        ( 7, 10, '112', '07:20', '00:10'),
        ( 7, 11, '101', '07:21', '00:10'),
        ( 7, 20, '124', '07:30', '00:10'),
        ( 7, 22, '150', '07:31', '00:09'),
        ( 7, 27, '102', '07:39', '00:12'),
        ( 7, 35, '124', '07:45', '00:10'),
        ( 7, 40, '112', '07:50', '00:10'),
        ( 7, 42, '150', '07:51', '00:09'),
        ( 7, 43, '124', '07:53', '00:10'),
        ( 7, 50, '124', '08:00', '00:10'),
        ( 7, 54, '124', '08:04', '00:10'),
        ( 7, 56, '112', '08:06', '00:10'),
        ( 7, 59, '112', '08:09', '00:10'),
        ( 8,  2, '111', '08:14', '00:12'),
        ( 8,  5, '124', '08:15', '00:10'),
        ( 8,  8, '112', '08:18', '00:10'),
        ( 8,  9, '124', '08:19', '00:10'),
        ( 8, 10, '112', '08:20', '00:10'),
        ( 8, 11, '101', '08:21', '00:10'),
        ( 8, 13, '112', '08:23', '00:10'),
        ( 8, 14, '112', '08:24', '00:10'),
        ( 8, 16, '112', '08:26', '00:10'),
        ( 8, 20, '124', '08:30', '00:10'),
        ( 8, 25, '111', '08:37', '00:12'),
        ( 8, 27, '102', '08:39', '00:12'),
        ( 8, 35, '124', '08:45', '00:10'),
        ( 8, 38, '112', '08:48', '00:10'),
        ( 8, 40, '112', '08:50', '00:10'),
        ( 8, 41, '101', '08:51', '00:10'),
        ( 8, 50, '124', '09:00', '00:10'),
        ( 8, 55, '111', '09:07', '00:12'),
        ( 8, 57, '102', '09:09', '00:12'),
        ( 9, 10, '112', '09:20', '00:10'),
        ( 9, 11, '101', '09:21', '00:10'),
        ( 9, 20, '124', '09:30', '00:10'),
        ( 9, 23, '111', '09:35', '00:12'),
        ( 9, 25, '111', '09:37', '00:12'),
        ( 9, 27, '102', '09:39', '00:12'),
        ( 9, 32, '112', '09:42', '00:10'),
        ( 9, 34, '112', '09:44', '00:10'),
        ( 9, 36, '150', '09:46', '00:10'),
        ( 9, 38, '112', '09:48', '00:10'),
        ( 9, 40, '112', '09:50', '00:10'),
        ( 9, 41, '101', '09:51', '00:10'),
        ( 9, 42, '112', '09:52', '00:10'),
        ( 9, 48, '112', '09:58', '00:10'),
        ( 9, 50, '124', '10:00', '00:10'),
        ( 9, 55, '111', '10:07', '00:12'),
        ( 9, 57, '102', '10:09', '00:12'),
        (10, 10, '112', '10:20', '00:10'),
        (10, 11, '101', '10:21', '00:10'),
        (10, 20, '124', '10:30', '00:10'),
        (10, 27, '102', '10:39', '00:12'),
        (10, 35, '111', '10:47', '00:12'),
        (10, 40, '112', '10:50', '00:10'),
        (10, 41, '101', '10:51', '00:10'),
        (10, 50, '124', '11:00', '00:10'),
        (10, 52, '150', '11:01', '00:09'),
        (10, 57, '102', '11:09', '00:12'),
        (11,  5, '111', '11:17', '00:12'),
        (11, 10, '112', '11:20', '00:10'),
        (11, 11, '101', '11:21', '00:10'),
        (11, 20, '124', '11:30', '00:10'),
        (11, 27, '102', '11:39', '00:12'),
        (11, 35, '111', '11:47', '00:12'),
        (11, 40, '112', '11:50', '00:10'),
        (11, 41, '101', '11:51', '00:10'),
        (11, 50, '124', '12:00', '00:10'),
        (11, 57, '102', '12:09', '00:12'),
        (12,  5, '111', '12:17', '00:12'),
        (12, 10, '112', '12:20', '00:10'),
        (12, 11, '101', '12:21', '00:10'),
        (12, 20, '124', '12:30', '00:10'),
        (12, 27, '102', '12:39', '00:12'),
        (12, 35, '111', '12:47', '00:12'),
        (12, 40, '112', '12:50', '00:10'),
        (12, 41, '101', '12:51', '00:10'),
        (12, 50, '124', '13:00', '00:10'),
        (12, 52, '150', '13:01', '00:09'),
        (12, 57, '102', '13:09', '00:12'),
        (13,  5, '111', '13:17', '00:12'),
        (13, 10, '112', '13:20', '00:10'),
        (13, 11, '101', '13:21', '00:10'),
        (13, 20, '124', '13:30', '00:10'),
        (13, 27, '102', '13:39', '00:12'),
        (13, 35, '111', '13:47', '00:12'),
        (13, 40, '112', '13:50', '00:10'),
        (13, 42, '150', '13:51', '00:09'),
        (13, 50, '124', '14:00', '00:10'),
        (13, 57, '102', '14:09', '00:12'),
        (14,  5, '111', '14:17', '00:12'),
        (14, 10, '112', '14:20', '00:10'),
        (14, 11, '101', '14:21', '00:10'),
        (14, 20, '124', '14:30', '00:10'),
        (14, 27, '102', '14:39', '00:12'),
        (14, 35, '111', '14:47', '00:12'),
        (14, 40, '112', '14:50', '00:10'),
        (14, 41, '101', '14:51', '00:10'),
        (14, 47, '124', '14:57', '00:10'),
        (14, 48, '109', '15:00', '00:12'),
        (14, 57, '102', '15:09', '00:12'),
        (15,  2, '124', '15:12', '00:10'),
        (15,  5, '111', '15:17', '00:12'),
        (15, 10, '112', '15:20', '00:10'),
        (15, 11, '101', '15:21', '00:10'),
        (15, 17, '124', '15:27', '00:10'),
        (15, 18, '109', '15:30', '00:12'),
        (15, 27, '102', '15:39', '00:12'),
        (15, 32, '124', '15:42', '00:10'),
        (15, 35, '111', '15:47', '00:12'),
        (15, 40, '112', '15:50', '00:10'),
        (15, 41, '101', '15:51', '00:10'),
        (15, 47, '124', '15:57', '00:10'),
        (15, 48, '109', '16:00', '00:12'),
        (15, 57, '102', '16:09', '00:12'),
        (16,  2, '124', '16:12', '00:10'),
        (16,  5, '111', '16:17', '00:12'),
        (16, 10, '112', '16:20', '00:10'),
        (16, 11, '101', '16:21', '00:10'),
        (16, 17, '124', '16:27', '00:10'),
        (16, 18, '109', '16:30', '00:12'),
        (16, 27, '102', '16:39', '00:12'),
        (16, 32, '124', '16:42', '00:10'),
        (16, 37, '150', '16:46', '00:09'),
        (16, 40, '112', '16:50', '00:10'),
        (16, 41, '101', '16:51', '00:10'),
        (16, 47, '124', '16:57', '00:10'),
        (16, 48, '109', '17:00', '00:12'),
        (16, 57, '102', '17:09', '00:12'),
        (17,  2, '124', '17:12', '00:10'),
        (17,  5, '111', '17:17', '00:12'),
        (17, 10, '112', '17:20', '00:10'),
        (17, 11, '101', '17:21', '00:10'),
        (17, 17, '124', '17:27', '00:10'),
        (17, 18, '109', '17:30', '00:12'),
        (17, 27, '102', '17:39', '00:12'),
        (17, 32, '124', '17:42', '00:10'),
        (17, 35, '111', '17:47', '00:12'),
        (17, 40, '112', '17:50', '00:10'),
        (17, 41, '101', '17:51', '00:10'),
        (17, 47, '124', '17:57', '00:10'),
        (17, 48, '109', '18:00', '00:12'),
        (17, 57, '102', '18:09', '00:12'),
        (18,  2, '124', '18:12', '00:10'),
        (18,  5, '111', '18:17', '00:12'),
        (18, 11, '101', '18:21', '00:10'),
        (18, 17, '124', '18:27', '00:10'),
        (18, 18, '109', '18:30', '00:12'),
        (18, 27, '102', '18:39', '00:12'),
        (18, 32, '124', '18:42', '00:10'),
        (18, 35, '111', '18:47', '00:12'),
        (18, 41, '101', '18:51', '00:10'),
        (18, 47, '124', '18:57', '00:10'),
        (18, 48, '109', '19:00', '00:12'),
        (18, 52, '150', '19:01', '00:09'),
        (18, 57, '102', '19:09', '00:12'),
        (19,  2, '124', '19:12', '00:10'),
        (19, 11, '101', '19:21', '00:10'),
        (19, 17, '124', '19:27', '00:10'),
        (19, 27, '102', '19:39', '00:12'),
        (19, 41, '101', '19:51', '00:10'),
        (19, 47, '124', '19:57', '00:10'),
        (19, 57, '102', '20:09', '00:12'),
        (20, 11, '101', '20:21', '00:10'),
        (20, 22, '150', '20:31', '00:09'),
        (20, 27, '102', '20:39', '00:12'),
        (21,  2, '101', '21:12', '00:10'),
        (21, 30, '102', '21:41', '00:11'),
        (22,  2, '101', '22:12', '00:10'),
        (22, 30, '102', '22:41', '00:11'),
        (23,  2, '101', '23:12', '00:10'),
        (23, 30, '102', '23:41', '00:11'),
        (23, 47, '103', '00:12', '00:25')]
    else:
        tms = [( 9,  2, '112', '09:14', '00:12'),
        ( 9,  8, '150', '09:18', '00:10'),
        ( 9, 18, '112', '09:30', '00:12'),
        ( 9, 25, '111', '09:38', '00:13'),
        ( 9, 27, '101', '09:39', '00:12'),
        ( 9, 32, '112', '09:44', '00:12'),
        ( 9, 38, '124', '09:50', '00:12'),
        ( 9, 47, '102', '10:00', '00:13'),
        ( 9, 55, '111', '10:08', '00:13'),
        ( 9, 57, '101', '10:09', '00:12'),
        (10,  2, '112', '10:14', '00:12'),
        (10, 10, '150', '10:20', '00:10'),
        (10, 17, '102', '10:30', '00:13'),
        (10, 25, '111', '10:38', '00:13'),
        (10, 27, '101', '10:39', '00:12'),
        (10, 32, '112', '10:44', '00:12'),
        (10, 38, '124', '10:50', '00:12'),
        (10, 47, '102', '11:00', '00:13'),
        (10, 55, '111', '11:08', '00:13'),
        (10, 57, '101', '11:09', '00:12'),
        (11,  2, '112', '11:14', '00:12'),
        (11,  8, '124', '11:20', '00:12'),
        (11, 17, '102', '11:30', '00:13'),
        (11, 25, '111', '11:38', '00:13'),
        (11, 27, '101', '11:39', '00:12'),
        (11, 32, '112', '11:44', '00:12'), 
        (11, 38, '124', '11:50', '00:12'), 
        (11, 47, '102', '12:00', '00:13'), 
        (11, 55, '111', '12:08', '00:13'), 
        (11, 57, '101', '12:09', '00:12'), 
        (12,  2, '112', '12:14', '00:12'), 
        (12,  8, '124', '12:20', '00:12'), 
        (12, 17, '102', '12:30', '00:13'), 
        (12, 25, '111', '12:38', '00:13'), 
        (12, 29, '150', '12:39', '00:10'), 
        (12, 32, '112', '12:44', '00:12'), 
        (12, 38, '124', '12:50', '00:12'), 
        (12, 47, '102', '13:00', '00:13'), 
        (12, 55, '111', '13:08', '00:13'), 
        (12, 57, '101', '13:09', '00:12'), 
        (13,  2, '112', '13:14', '00:12'), 
        (13,  8, '124', '13:20', '00:12'), 
        (13, 17, '102', '13:30', '00:13'), 
        (13, 23, '150', '13:33', '00:10'), 
        (13, 25, '111', '13:38', '00:13'), 
        (13, 27, '101', '13:39', '00:12'), 
        (13, 32, '112', '13:44', '00:12'), 
        (13, 38, '124', '13:50', '00:12'), 
        (13, 47, '102', '14:00', '00:13'), 
        (13, 55, '111', '14:08', '00:13'), 
        (13, 57, '101', '14:09', '00:12'), 
        (14,  2, '112', '14:14', '00:12'), 
        (14,  8, '124', '14:20', '00:12'), 
        (14, 17, '102', '14:30', '00:13'), 
        (14, 25, '111', '14:38', '00:13'), 
        (14, 27, '101', '14:39', '00:12'), 
        (14, 32, '112', '14:44', '00:12'), 
        (14, 38, '124', '14:50', '00:12'), 
        (14, 47, '102', '15:00', '00:13'), 
        (14, 55, '111', '15:08', '00:13'), 
        (14, 57, '101', '15:09', '00:12'), 
        (15,  2, '112', '15:14', '00:12'), 
        (15,  5, '124', '15:17', '00:12'), 
        (15,  7, '109', '15:20', '00:13'), 
        (15, 17, '102', '15:30', '00:13'), 
        (15, 20, '124', '15:32', '00:12'), 
        (15, 25, '111', '15:38', '00:13'), 
        (15, 27, '101', '15:39', '00:12'), 
        (15, 32, '112', '15:44', '00:12'), 
        (15, 35, '124', '15:47', '00:12'), 
        (15, 37, '109', '15:50', '00:13'), 
        (15, 47, '102', '16:00', '00:13'), 
        (15, 53, '124', '16:05', '00:12'), 
        (15, 55, '111', '16:08', '00:13'), 
        (15, 57, '101', '16:09', '00:12'), 
        (16,  2, '112', '16:14', '00:12'), 
        (16,  5, '124', '16:17', '00:12'), 
        (16,  7, '109', '16:20', '00:13'), 
        (16, 13, '150', '16:23', '00:10'), 
        (16, 17, '102', '16:30', '00:13'), 
        (16, 20, '124', '16:32', '00:12'), 
        (16, 25, '111', '16:38', '00:13'), 
        (16, 27, '101', '16:39', '00:12'), 
        (16, 32, '112', '16:44', '00:12'), 
        (16, 35, '124', '16:47', '00:12'), 
        (16, 37, '109', '16:50', '00:13'), 
        (16, 47, '102', '17:00', '00:13'), 
        (16, 50, '124', '17:02', '00:12'), 
        (16, 55, '111', '17:08', '00:13'), 
        (16, 57, '101', '17:09', '00:12'), 
        (17,  2, '112', '17:14', '00:12'), 
        (17,  5, '124', '17:17', '00:12'), 
        (17,  7, '109', '17:20', '00:13'), 
        (17, 17, '102', '17:30', '00:13'), 
        (17, 20, '124', '17:32', '00:12'), 
        (17, 25, '111', '17:38', '00:13'), 
        (17, 27, '101', '17:39', '00:12'), 
        (17, 32, '112', '17:44', '00:12'), 
        (17, 35, '124', '17:47', '00:12'), 
        (17, 37, '109', '17:50', '00:13'), 
        (17, 47, '102', '18:00', '00:13'), 
        (17, 53, '124', '18:05', '00:12'), 
        (17, 55, '111', '18:08', '00:13'), 
        (17, 57, '101', '18:09', '00:12'), 
        (18,  2, '112', '18:14', '00:12'), 
        (18,  5, '124', '18:17', '00:12'), 
        (18,  7, '109', '18:20', '00:13'), 
        (18, 17, '102', '18:30', '00:13'), 
        (18, 20, '124', '18:32', '00:12'), 
        (18, 25, '111', '18:38', '00:13'), 
        (18, 27, '101', '18:39', '00:12'), 
        (18, 35, '124', '18:47', '00:12'), 
        (18, 37, '109', '18:50', '00:13'), 
        (18, 47, '102', '19:00', '00:13'), 
        (18, 50, '124', '19:02', '00:12'), 
        (18, 55, '111', '19:08', '00:13'), 
        (18, 57, '101', '19:09', '00:12'), 
        (19,  5, '124', '19:17', '00:12'), 
        (19,  7, '109', '19:20', '00:13'), 
        (19, 17, '102', '19:30', '00:13'), 
        (19, 20, '124', '19:32', '00:12'), 
        (19, 23, '150', '19:33', '00:10'), 
        (19, 27, '101', '19:39', '00:12'), 
        (19, 35, '124', '19:47', '00:12'), 
        (19, 47, '102', '20:00', '00:13'), 
        (19, 57, '101', '20:09', '00:12'), 
        (20,  5, '124', '20:17', '00:12'), 
        (20, 17, '102', '20:30', '00:13'), 
        (20, 27, '101', '20:39', '00:12'), 
        (20, 40, '102', '20:52', '00:12'), 
        (20, 57, '101', '21:09', '00:12'), 
        (21, 12, '102', '21:24', '00:12'), 
        (21, 41, '101', '21:51', '00:10'), 
        (22, 12, '102', '22:24', '00:12'),
        (22, 41, '101', '22:51', '00:10'),
        (23, 12, '102', '23:24', '00:12'),
        (23, 41, '101', '23:51', '00:10')]

    # remove trailing seconds
    import re
    reg = re.compile(r':00$')

    def min_subtract(hour, mins, walking_time):
        mins = mins - walking_time
        if mins < 0:
            hour -= 1
            mins = 60 + mins
        return hour, mins

    def mins_to_go(currenttime, bustime):
        ttg = datetime.datetime(1, 1, 1, bustime.hour, bustime.minute) - datetime.datetime(1, 1, 1, currenttime.hour, currenttime.minute)
        m = int(ttg.total_seconds() / 60)
        h = m / 60
        m = m / (h + 1)
        return '%s:%s' % (str(h).zfill(2), str(m).zfill(2))

    # get string current time
    from time import strftime, localtime

    # set direction string
    if where == 'u':
        direction = 'University --> Blumenstr.'
    else:
        direction = 'Blumenstr. --> University'

    # print header
    print '\n================================'\
          '\nCurrently: %s, %s'\
          '\n--------------------------------'\
          '\n%s (w=%s)'\
          '\n--------------------------------' % (day, strftime("%H:%M:%S", localtime()), direction, str(walking_time).zfill(2))
    print 'Time   Bus    Arr.   Dur.     In'\
          '\n--------------------------------'
    
    # check if bus is upcoming
    shown = 0
    for hour, minu, bus_num, arr_str, duration in tms:
        # actual bus time
        oldt = datetime.time(hour, minu)
        hour, minu = min_subtract(hour, minu, walking_time)
        # fake time with walking time into account
        t = datetime.time(hour, minu)

        nbus = int(nbus)
        # show nbus
        if shown < nbus:
            if t > now:
                diff = datetime.datetime(1, 1, 1, oldt.hour, oldt.minute) - datetime.datetime(1, 1, 1, now.hour, now.minute)
                shown += 1
                form_time = re.sub(reg, '', str(oldt))
                addline = False
                if bus_num not in ['102', '109', '111']:
                    addline = True
                    bus_num = bus_num + '*'
                else:
                    bus_num = bus_num + ' '
                m_to_go = mins_to_go(now, oldt)
                print '%s  %s  %s  %s  %s' % (form_time, bus_num, arr_str, duration, re.sub(reg, '', str(diff)).zfill(5))
    # closing lines
    print '\n* Dudweilerstr. bus stop\n================================\n'

# allow run from cmd line
if __name__ == '__main__':
    
    import sys

    def is_number(s):
        """check if str can be can be made into float/int"""
        try:
            float(s) # for int, long and float
        except ValueError:
            try:
                complex(s) # for complex
            except ValueError:
                return False
        return True

    if len(sys.argv) > 1 and is_number(sys.argv[1]):
        wt = {}
        if len(sys.argv) == 3:
            wt['walking_time'] = sys.argv[2]
        nextbus(where = 'guess', nbus = sys.argv[1], **wt)
    else:
        nextbus(*sys.argv[1:])
