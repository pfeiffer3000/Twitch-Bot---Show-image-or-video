
from twitchio.ext import commands, eventsub
import cv2

# get your Twitch token
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"   # e.g. "3y3lcqp6l39zwvt1furi9ldr55kekef92"
USERS_CHANNEL_ID = "YOUR_CHANNEL_ID" # e.g. "714693512"

# list the channels you want to connect to (e.g. ['djpfeifdnb', 'htpbot'])
initial_channels = ['your_channel_1', 'your_channel_2', 'etc'] 


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix="!", initial_channels=initial_channels)
        self.esclient = eventsub.EventSubWSClient(self)
    

    async def event_ready(self):
        channel = await self.fetch_channels([USERS_CHANNEL_ID])
        print(f"{channel[0].title = }")
        print()
        print(f'Logged in as | {self.nick}')
        print(f'User id is   | {self.user_id}')
        print(f"Ready!")
        print()
        

    async def event_message(self, message):
        if message.echo:
            # Print messages from the bot to the console, but don't process them for commands and such.
            print(f"    {self.nick}: {message.content}")
            return
  
        # Print the contents of our message to console
        print(f"{message.author.name}: {message.content}")
        
        # check for special words that trigger actions
        # in this case, check to see if "mugtion" or "backrooms" is in the message
        if "mugtion" in message.content.lower():
            await self.show_image()
        elif "backrooms" in message.content.lower():
            await self.play_video() 
        
        await self.handle_commands(message)

        
    async def play_video(self):
        """
        Plays a video file.
        :return: None

        Set the window_name to something unique so OBS can find it and display it.
        """

        file = "backrooms_video.mp4"

        video = cv2.VideoCapture(file)  # handles the video
        fps = video.get(cv2.CAP_PROP_FPS) 

        print(f"======Playing video: {file}======")
        while video.isOpened():
            ret, frame = video.read()  # ret is bool, "returned" value. It's false if there is no next frame to read
            
            # quit stuff
            if not ret:
                print("End of Video")
                break
            wait_time = int(400 / fps)  # wait time in milliseconds
            if cv2.waitKey(wait_time) & 0xFF==ord('q'):  # press q to quit the playback
                break

            # resize the frame
            width = 480
            height = 270
            frame = cv2.resize(frame, (width, height))

            # display the video
            window_name = "Bot Video Unique Name"
            cv2.imshow(window_name, frame)   # display the video

        video.release()
        cv2.destroyAllWindows()

    async def show_image(self):
        """
        Displays an image for a given amount of time.
        :return: None

        Set the window_name to something unique so OBS can find it and display it.
        """      

        image_path = "mugtion - 768x.png"
        wait_time = 3000 # show the image for 3 seconds

        img = cv2.imread(image_path)
        if img is not None:
            # resize the image if needed
            width = 512
            height = 512
            img = cv2.resize(img, (width, height))

            window_name = "Bot Image Unique Name"
            cv2.imshow(window_name, img) 

            key = cv2.waitKey(wait_time) & 0xFF==ord('q')  # press q to close the image

            cv2.destroyAllWindows()
            print(f"==Displayed: {image_path}")
        else:
            print(f"Pferror: unable to display the image.")


bot = Bot()
bot.run()
