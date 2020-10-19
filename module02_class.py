from datetime import datetime, tzinfo, timedelta
''' Converts the date to ISO 8601 format
Segro team, S2DS August 2020 - Aug. 13, 2020
Contact: M. Fortin, D. Muller
Partly based on https://stackoverflow.com/questions/46834202/how-to-convert-a-datetime-object-between-cest-and-utc-timezones'''
    
class CET(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=1) + self.dst(dt)

    def dst(self, dt):
        dston_20 = datetime(year=2020, month=3, day=29,hour=1)
        dstoff_20 = datetime(year=2020, month=10, day=25,hour=2)
        dston_19 = datetime(year=2019, month=3, day=31,hour=1)
        dstoff_19 = datetime(year=2019, month=10, day=27,hour=2)
        if dston_20 <= dt.replace(tzinfo=None) < dstoff_20:
            return timedelta(hours=1)
        elif dston_19 <= dt.replace(tzinfo=None) < dstoff_19:
            return timedelta(hours=1)
        else:
            return timedelta(0)

class BST(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=0) + self.dst(dt)

    def dst(self, dt):
        dston = datetime(year=dt.year, month=3, day=20)
        dstoff = datetime(year=dt.year, month=10, day=20)
        if dston <= dt.replace(tzinfo=None) < dstoff:
            return timedelta(hours=1)
        else:
            return timedelta(0)
        
class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)

    def dst(self, dt):
        return timedelta(0)

def from_cet_to_utc(year, month, day, hour, minute):
    cet = datetime(year, month, day, hour, minute, tzinfo=CET())
    utc = cet.astimezone(tz=UTC())
    return '{:%Y-%m-%dT%H:%M:%SZ}'.format(utc)

def from_bst_to_utc(year, month, day, hour, minute):
    cet = datetime(year, month, day, hour, minute, tzinfo=BST())
    utc = cet.astimezone(tz=UTC())
    return '{:%Y-%m-%dT%H:%M:%SZ}'.format(utc)

def from_date_to_iso(year=2020, month=8, day=19, hour=9, minute=0,location="UK"):
    '''returns the date to ISO 8601 format
    Input: year, month, day, hour, minute in local time **+ location in country code format**
    Output: date in ISO 8601 format'''
    
    if(year<=2018):
        print("Daily savings for years before 2019 not implemented")
        exit()
    elif location=="UK":
        return from_bst_to_utc(year, month, day, hour, minute)
    elif location in ["FR","DE","ES","IT","PL"]:
        return from_cet_to_utc(year, month, day, hour, minute)
    else:
        print("Your location is not supported (yet?)")
        exit()

def main():
    print("Default date in ISO format: "+from_date_to_iso())

if __name__ == "__main__":
    main()
