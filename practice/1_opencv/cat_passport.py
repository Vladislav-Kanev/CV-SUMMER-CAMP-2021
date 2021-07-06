import argparse
import sys
import cv2


def make_cat_passport_image(input_image_path, haar_model_path):

    # Read image
    image = cv2.imread(input_image_path)

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Normalize image intensity
    gray = cv2.equalizeHist(gray)

    # Resize image
    resized = cv2.resize(gray, (640, 480), interpolation = cv2.INTER_AREA)

    # Detect cat faces using Haar Cascade
    detector = cv2.CascadeClassifier(haar_model_path)
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                                      minSize=(75, 75))

    # Draw bounding box
    for (i, (x, y, w, h)) in enumerate(rects):
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(image, "Cat #{}".format(i + 1), (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

    # Display result image
    cv2.imshow("window_name", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Crop image
    x, y, w, h = rects[0]
    image = image[y:y + h, x:x + w]

    # Save result image to file
    cv2.imwrite('out.jpg', image)

    passport = cv2.imread('pet_passport.png')
    x1, y1, x2, y2 = 29, 46, 203, 188
    passport[y1:y2, x1:x2] = cv2.resize(image, (x2-x1, y2-y1), interpolation = cv2.INTER_AREA)
    cv2.putText(passport, "Barsik", (90, 215),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

    cv2.imshow("window_name", passport)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite('passport.jpg', passport)
    return


def build_argparser():
    parser = argparse.ArgumentParser(
        description='Speech denoising demo', add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                      help='Show this help message and exit.')
    args.add_argument('-m', '--model', type=str, required=True,
                      help='Required. Path to .XML file with pre-trained model.')
    args.add_argument('-i', '--input', type=str, required=True,
                      help='Required. Path to input image')
    return parser


def main():

    args = build_argparser().parse_args()
    make_cat_passport_image(args.input, args.model)

    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
