#!/bin/bash

for i in {1..5}
do
  # 测试 amz_to_ali 工作流
  curl -X POST \
    http://127.0.0.1:8081/workflow/run/amz_to_ali \
    -H 'Content-Type: application/json' \
    -d '{"imgs":["https://m.media-amazon.com/images/I/71DZ2v9NLEL._AC_SL1500_.jpg","https://m.media-amazon.com/images/I/61MztRfbfTL._AC_SL1500_.jpg","https://m.media-amazon.com/images/I/61sWQSYf1KL._AC_SL1500_.jpg","https://m.media-amazon.com/images/I/71zC2XGqoKL._AC_SL1500_.jpg"],"product_type":"card","price":"19.90","description":"About this item The Angelique Bach Flower Card Game is a playful and intuitive way to choose the flower elixir or elixirs that suit you. Beautiful box of 38 cards with an explanatory booklet Angelica Bach Flower maps can help us choose the floral elixirs we need. The goal is to find the remedy that corresponds to the negative state of mind that afflicts us. Among these states of mind we can mention: fear, worries, discouragement, uncertainty, etc.;. With these cards, it is easier to pinpoint these states of mind. allows us to recognize the states of being and behavioral patterns that distance us from our true nature. › See more product details","prodid":"https://www.amazon.fr/-/en/Bach-Flower-Cards-ILLUSTRATED-intuitively/dp/B0CN1HKKHP","reference_product_platform":"amazon","title":"Bach Flower Cards - 38 ILLUSTRATED CARDS - Set of 38 cards to intuitively select your Bach flowers","employee":"Alice","published_shop":"ali_shop2"}'
  echo -e "\n---\n"
#   sleep 1
done

for i in {1..5}
do
  # 测试 amz_to_1688 工作流
  curl -X POST \
    http://127.0.0.1:8081/workflow/run/amz_to_1688 \
    -H 'Content-Type: application/json' \
    -d '{"trace_id": "test-trace-1688-'"$i"'", "event_type": "amz_to_1688", "payload": {}}'
  echo -e "\n---\n"
#   sleep 1
done

for i in {1..5}
do
  # 测试 ali_to_1688 工作流
  curl -X POST \
    http://127.0.0.1:8081/workflow/run/ali_to_1688 \
    -H 'Content-Type: application/json' \
    -d '{"imgs":["https://s.alicdn.com/@sc04/kf/H8bea066d0dd94684beac3e999145efc5T.jpg","https://s.alicdn.com/@sc04/kf/H74a44201df394e4d8fdc1c9efb10ec96N.jpg","https://s.alicdn.com/@sc04/kf/H958d5ac0e6b44712ae94dbf55bf91585a.jpg","https://s.alicdn.com/@sc04/kf/H84777d5367764cf0a3f0c16ea2d47ad1x.jpg","https://s.alicdn.com/@sc04/kf/H7788f1e05e4841028782c96311c944a77.jpg","https://s.alicdn.com/@sc04/kf/H4a2f5a1e34e9435b9345d53c7317ad7du.jpg"],"product_type":"sticker","price":"","description":"","prodid":"https://www.alibaba.com/product-detail/Personalized-Metal-Sign-Vintage-Garage-Decorative_1601299327076.html","reference_product_platform":"ali","title":"Personalized Metal Sign Vintage Garage Decorative Poster Retro Metal Tin Plate Plaque Classic Coffee Metal Sign","employee":"thanos_zhang","published_shop":"1688shop3"}'
  echo -e "\n---\n"
#   sleep 1
done

for i in {1..5}
do
  # 测试 1688_to_1688 工作流
  curl -X POST \
    http://127.0.0.1:8081/workflow/run/1688_to_1688 \
    -H 'Content-Type: application/json' \
    -d '{"trace_id": "test-trace-1688to1688-'"$i"'", "event_type": "1688_to_1688", "payload": {}}'
  echo -e "\n---\n"
#   sleep 1
done

for i in {1..5}
do
  # 测试 ali_to_ali 工作流
  curl -X POST \
    http://127.0.0.1:8081/workflow/run/ali_to_ali \
    -H 'Content-Type: application/json' \
    -d '{"imgs":["https://s.alicdn.com/@sc04/kf/H8bea066d0dd94684beac3e999145efc5T.jpg","https://s.alicdn.com/@sc04/kf/H74a44201df394e4d8fdc1c9efb10ec96N.jpg","https://s.alicdn.com/@sc04/kf/H958d5ac0e6b44712ae94dbf55bf91585a.jpg","https://s.alicdn.com/@sc04/kf/H84777d5367764cf0a3f0c16ea2d47ad1x.jpg","https://s.alicdn.com/@sc04/kf/H7788f1e05e4841028782c96311c944a77.jpg","https://s.alicdn.com/@sc04/kf/H4a2f5a1e34e9435b9345d53c7317ad7du.jpg"],"product_type":"sticker","price":"","description":"","prodid":"https://www.alibaba.com/product-detail/Personalized-Metal-Sign-Vintage-Garage-Decorative_1601299327076.html","reference_product_platform":"ali","title":"Personalized Metal Sign Vintage Garage Decorative Poster Retro Metal Tin Plate Plaque Classic Coffee Metal Sign","employee":"thanos_zhang","published_shop":"ali_shop2"}'
  echo -e "\n---\n"
#   sleep 1
done

# 测试 social_to_ali 工作流
curl -X POST \
    http://127.0.0.1:8081/workflow/run/social_to_ali \
    -H 'Content-Type: application/json' \
    -d '{"platform": "tiktok", "page_size": 30}'
echo -e "\n---\n"

# 查询状态
# curl localhost:8081/workflows/<trace_id>/status

# 重试任务
# curl -X POST http://localhost:8081/workflows/tasks/retry/f5a7259e-2b26-44cd-928c-c68790b61c8c
