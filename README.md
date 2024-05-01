## Labelme_Augumentation

## 사용법

[data_augmentation_flipped.py](data_augmentation_flipped.py)

```python
python data_augmentation_flipped.py --input_folder "./path/to/input" --output_folder "./path/to/output" --flip_mode "horizontal"
```

<br>

[data_augmentation_rotate.py](data_augmentation_rotate.py)

```python
python data_augmentation_rotate.py --input_dir "./path/to/input_directory" --output_image_dir "./path/to/output_images" --output_label_dir "./path/to/output_labels" --rotation_step 15
```

<br>

### YOLO 학습을 위한 어노테이션 자료의 데이터 증강

* 바운딩 박스의 좌표를 정의하는 방법은 두가지가 있음.
* (x1, y1, w, h)와 (xmin, ymin, xmax, ymax)
  
![image](https://github.com/EthanSeok/Labelme_Augumentation/assets/93086581/58d299f7-5cba-40fd-900d-e0e58c48210c)

<br>

### Labelme JSON 포맷

```
{
  "version": "4.2.10",
  "flags": {},
  "shapes": [
    {
      "label": "dog",
      "points": [[125, 120], [185, 220], [228, 119]],
      "group_id": null,
      "shape_type": "polygon",
      "flags": {}
    },
    {
      "label": "cat",
      "points": [[50, 50], [50, 100], [100, 100], [100, 50]],
      "group_id": 1,
      "shape_type": "rectangle",
      "flags": {}
    }
  ],
  "imagePath": "path_to_image.jpg",
  "imageData": null,
  "imageHeight": 800,
  "imageWidth": 600
}
```

* **imageData에 base64로 인코딩된 이미지 자료가 있어야 함.**

<br>

## 회전 
[https://blog.roboflow.com/why-and-how-to-implement-random-rotate-data-augmentation/](https://blog.roboflow.com/why-and-how-to-implement-random-rotate-data-augmentation/) 참고

<br>

## 결과
![image](https://github.com/EthanSeok/Labelme_Augumentation/assets/93086581/b7677d14-16a3-4709-8289-c1b6c7812c36)
