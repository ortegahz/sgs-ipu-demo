#!/bin/bash

MODEL_NAME="$1"
INPUT_SHAPE=1,3,480,640
PREPROCESS_NAME="yolov5_onnx_640"
if [ "$2" == "640" ]; then
  INPUT_SHAPE=1,3,480,640
  PREPROCESS_NAME="yolov5_onnx_640"
elif [ "$2" == "960" ]; then
  INPUT_SHAPE=1,3,736,960
  PREPROCESS_NAME="yolov5_onnx_960"
elif [ "$2" == "320" ]; then
  INPUT_SHAPE=1,3,256,320
  PREPROCESS_NAME="yolov5_onnx_320256"
elif [ "$2" == "320320" ]; then
  INPUT_SHAPE=1,3,320,320
  PREPROCESS_NAME="yolov5_onnx_320320"
else
  echo "Error: Invalid second argument. Please use 640(for 480 x 640), 960(for 736 x 960), or 320(for 256 x 320), or 320320(for 320 x 320)."
  exit 1
fi

python3 Scripts/ConvertTool/ConvertTool.py onnx \
  --model_file "./Conversion/Models/${MODEL_NAME}/${MODEL_NAME}.onnx" \
  --input_arrays image \
  --input_shapes "$INPUT_SHAPE" \
  --output_arrays output0,output1,output2 \
  --input_config Conversion/input_config_yolov5.ini \
  --output_file "./Conversion/mid_sim/${MODEL_NAME}.onnx.sim"
python3 Scripts/calibrator/calibrator.py \
  -i "Conversion/Models/${MODEL_NAME}/images/" \
  -m "./Conversion/mid_sim/${MODEL_NAME}.onnx.sim" \
  -c Unknown \
  --input_config Conversion/input_config_yolov5.ini \
  -n "$PREPROCESS_NAME"
python3 Scripts/calibrator/compiler.py -m "./Conversion/mid_sim/${MODEL_NAME}.onnx_fixed.sim"

mv "./Conversion/mid_sim/${MODEL_NAME}.onnx_fixed.sim_sgsimg.img" "./Conversion/Models/${MODEL_NAME}/${MODEL_NAME}.onnx_fixed.sim_sgsimg.img"
echo "Finished Converting. Located at ./Conversion/Models/${MODEL_NAME}/${MODEL_NAME}.onnx_fixed.sim_sgsimg.img"
