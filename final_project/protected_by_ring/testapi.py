import json
import getpass
from pathlib import Path
from pprint import pprint

from ring_doorbell import Ring, Auth
from oauthlib.oauth2 import MissingTokenError


cache_file = Path("test_token.cache")


def token_updated(token):
    cache_file.write_text(json.dumps(token))


def otp_callback():
    auth_code = input("2FA code: ")
    return auth_code


def sign_in_get_devices():
    if cache_file.is_file():
        auth = Auth("protected-by-ring/1.0", json.loads(cache_file.read_text()), token_updated)
    else:

        # username = input("Username: ")
        username = 'nonmodernity@gmail.com'
        # password = getpass.getpass("Password: ")
        password = 'N3wpassword!' #wevene<3rBeenModern'
        auth = Auth("protected-by-ring/1.0", None, token_updated)
        try:
            auth.fetch_token(username, password)
        except MissingTokenError:
            auth.fetch_token(username, password, otp_callback())

    ring = Ring(auth)
    ring.update_data()

    devices = ring.devices()
    doorbell = devices['doorbots'][0]  # this is a list but we just have 1 doorbell
    pprint(doorbell)
    return doorbell


def get_doorbell_attributes(doorbell):
    doorbell.update_health_data()
    print('Address:    %s' % doorbell.address)
    print('Family:     %s' % doorbell.family)
    print('ID:         %s' % doorbell.id)
    print('Name:       %s' % doorbell.name)
    print('Timezone:   %s' % doorbell.timezone)
    print('Wifi Name:  %s' % doorbell.wifi_name)
    print('Wifi RSSI:  %s' % doorbell.wifi_signal_strength)

    # setting dev volume
    print('Volume:     %s' % doorbell.volume)


def get_doorbell_events(doorbell):
    print('--' * 23, 'Events', '--' * 23)
    # listing the last 15 events of any kind
    for event in doorbell.history(limit=15):
        print('ID:       %s' % event['id'])
        print('Kind:     %s' % event['kind'])
        print('Answered: %s' % event['answered'])
        print('When:     %s' % event['created_at'])
        print('--' * 50)

    # # get a event list only the triggered by motion
    # events = doorbell.history(kind='motion')


def get_latest_video(doorbell):
    print("downloading...")
    filename = './last_ding.mp4'
    doorbell.recording_download(doorbell.history(limit=10, kind='ding')[0]['id'], filename=filename, override=True)
    print("Downloaded locally: ", filename)


def latest_video_url(doorbell):
    # provides an aws link to the latest video...
    print(doorbell.recording_url(doorbell.last_recording_id))


def main():
    doorbell = sign_in_get_devices()
    get_doorbell_attributes(doorbell)
    get_doorbell_events(doorbell)
    get_latest_video(doorbell)
    latest_video_url(doorbell)


if __name__ == "__main__":
    main()
