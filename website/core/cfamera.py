import cv2              as cv 
import numpy            as np
from website.settings   import BASE_DIR
from keras.models       import load_model
from .models            import fire
from django.core.files  import File



class GetCamera:
    def __init__(self , source = 0):
        self.model          = load_model(BASE_DIR/'AI'/'flame_smoke_detection_model.h5')
        self.video          = cv.VideoCapture(source)
        self.record         = False
        self.video_saving   = []

    def preprocess_frame(self,frame):
        resized_frmae       = cv.resize(frame , (400,400))
        normalized_frame    = resized_frmae / 255.0
        input_frame         = np.expand_dims(normalized_frame , axis=0)
        return input_frame

    def __del__(self):
        self.video.release()

    def save_video(self , number):
        if self.video_saving:
            temp = fire(
                file        = None,
                percentage  = number,
            )

            height , width , _ = self.video_saving[0].shape
            fourcc          = cv.VideoWriter_fourcc(*'mp4v')
            path            = BASE_DIR / 'media' / 'firevideos' / 'temp.mp4'
            out             = cv.VideoWriter(str(path) , fourcc , 20.0 , (width , height))
            for frame in self.video_saving:
                out.write(frame)
            out.release()
            self.video_saving  = []

            with open(path , 'rb') as vfile :
                temp.file.save(f'video_{temp.id}.mp4', File(vfile))
                temp.save()
                print("done fiel :" , temp.id)


    def get_frame(self):
        success , frame     = self.video.read()
        if not success:
            return None
        
        input_frame         = self.preprocess_frame(frame)
        prediction          = self.model.predict(input_frame)

        if prediction > 0.65:
            self.record = True 
            self.video_saving.append(frame.copy())
            cv.putText(frame , f"Fire/Smoke : {str(prediction)[:4]}" , (10 , 50) , cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
        else:
            if self.record:
                self.save_video(prediction)
                self.record = False

            cv.putText(frame, 'No Fire/Smoke', (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
        _ , jpg             = cv.imencode('.jpg' , frame)
        return jpg.tobytes()
    
    def gen_frame(self):
        while True:
            frame = self.get_frame()
            if frame is not None:
                yield(
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
                )