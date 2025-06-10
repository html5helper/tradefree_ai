from fastapi import FastAPI, Request, Depends
from ai.core.history.task_retry import retry_chain_by_task_id
from ai.core.celery_workflow import CeleryWorkflow
from ai.core.auth.authentication import verify_token

api = FastAPI()
workflow = CeleryWorkflow()

@api.post("/workflow/run/copy")
async def copy(request: Request, access: dict = Depends(verify_token)):
    """Copy and public product workflow"""
    data = await request.json()
    workflow_name = access.get("workflow", "")
    
    if not workflow_name:
        return {"error": "Invalid workflow"}
    return workflow.create_workflow(workflow_name, data)
    
@api.post("/workflow/run/copy_no_ai")
async def copy_no_ai(request: Request, access: dict = Depends(verify_token)):
    """Copy and public product workflow no ai"""
    data = await request.json()
    data['use_ai'] = 'false'
    workflow_name = access.get("workflow", "")
    
    if not workflow_name:
        return {"error": "Invalid workflow"}
    return workflow.create_workflow(workflow_name, data)

@api.post("/workflow/run/social_to_ali")
async def social_to_ali(request: Request, user_info: dict = Depends(verify_token)):
    """Social to AliExpress workflow"""
    data = await request.json()
    return workflow.create_workflow("social_total", data)

@api.post("/workflow/tasks/retry/{task_id}")
async def retry_task(task_id: str):
    """Retry a failed task and its downstream tasks"""
    return {"task_id": retry_chain_by_task_id(task_id)}
 
@api.post("/workflow/product/list")
async def product_list(request: Request, user_info: dict = Depends(verify_token)):
    """Product list"""
    try:
        data = await request.json()
    except:
        data = {}
    res = [
        {
            "title": "Outdoor UV Resist Impermeável À Prova D' Água Pvc Estética Adesivo Qr Código Adesivo Logotipo Personalizado Die Cut Vinyl Label Adesivos",
            "description": "Elevate your branding with our Custom UV Resistant Waterproof PVC QR Code Logo Stickers, designed for durability and versatility in both indoor and outdoor environments. These stickers are crafted from high-quality waterproof PVC material that resists fading from UV exposure, making them perfect for long-term use on signage, promotional materials, or product packaging. Each sticker features a die-cut design that ensures a clean, professional look when applied, while the embedded QR code allows for seamless digital engagement—directing users to websites, social media pages, or promotional content. The waterproof and weather-resistant properties of these stickers make them ideal for use on vehicles, billboards, banners, or even as part of event promotions. Available in a range of sizes and customizable with your logo or text, they offer a modern, sleek appearance that blends functionality with visual appeal. Whether you're promoting a business, launching a new product, or creating interactive marketing content, these stickers provide a cost-effective and eye-catching solution. Their easy-to-apply adhesive ensures a secure bond without leaving residue, and their vibrant colors remain sharp even under harsh conditions. Perfect for businesses looking to enhance visibility and customer interaction through innovative, durable, and stylish sticker solutions.",
            "price": "0.8",
            "moq": "200",
            "imgs": [
            "/opt/data/img/ffb2925b-f684-4810-8e40-15b287bb6c31/1749282239948_9589.png",
            "/opt/data/img/ffb2925b-f684-4810-8e40-15b287bb6c31/1749282240828_9949.png",
            "/opt/data/img/ffb2925b-f684-4810-8e40-15b287bb6c31/1749282241805_1320.png",
            "/opt/data/img/ffb2925b-f684-4810-8e40-15b287bb6c31/1749282242107_3965.png",
            "/opt/data/img/ffb2925b-f684-4810-8e40-15b287bb6c31/1749282243485_4645.png",
            "/opt/data/img/ffb2925b-f684-4810-8e40-15b287bb6c31/1749282244219_4672.png"
            ],
            "product_type": "sticker",
            "delivery_time": "7 days",
            "reference_product": "https://www.alibaba.com/product-detail/Outdoor-UV-Resist-Waterproof-Weatherproof-Pvc_1600994418432.html",
            "reference_product_platform": "ali",
            "employee": "1688【丰和金-张姗】",
            "published_shop": "ali_shop2",
            "trace_id": "8551396b-5e26-447d-bd3f-3515801882c1",
            "workflow_name": "ali_to_ali",
            "task_id": "a949d73f-d87c-4816-85f0-4a06e0f154fb",
            "shot_description": "Custom UV Resistant Waterproof PVC QR Code Logo Stickers - Made from durable waterproof PVC material, these stickers resist fading and are suitable for both indoor and outdoor use. They feature a die-cut design with a custom QR code and logo, ideal for branding on signage, promotional materials, or product packaging. Easy to apply and long-lasting, they are perfect for enhancing visibility and digital engagement.",
            "applicable_scenes": "",
            "tags": "custom qr code stickers waterproof vinyl labels uv resistant pvc stickers die cut logo stickers outdoor signage stickers waterproof qr code stickers promotional stickers die cut vinyl labels brand logo stickers durable waterproof stickers",
            "product_name": "Custom UV Resistant Waterproof PVC QR Code Logo Sticker",
            "code": 200,
            "short_description": "",
            "title_mask_count": 0,
            "description_mask_count": 0,
            "short_description_mask_count": 0,
            "str_photos": "id_5=13905901052,id_4=13905853424,url_4=https://sc04.alicdn.com/kf/H321110515ce04c0280ef190addb67ee6U/231139578/H321110515ce04c0280ef190addb67ee6U.png,url_5=https://sc04.alicdn.com/kf/H9ab134feb46f4844a38b853339b3c36eA/231139578/H9ab134feb46f4844a38b853339b3c36eA.png,url_2=https://sc04.alicdn.com/kf/Hfa4fffc851c049bea8c563bf3d63323dX/231139578/Hfa4fffc851c049bea8c563bf3d63323dX.png,url_3=https://sc04.alicdn.com/kf/Hb85334ae787a44009edff87c41e91a98W/231139578/Hb85334ae787a44009edff87c41e91a98W.png,url_0=https://sc04.alicdn.com/kf/Hde59891a2e03463b9ee9b5ea630577fbu/231139578/Hde59891a2e03463b9ee9b5ea630577fbu.png,url_1=https://sc04.alicdn.com/kf/H8e745b0abd684df5a73dd6d9eba6eb3dg/231139578/H8e745b0abd684df5a73dd6d9eba6eb3dg.png,id_1=13905901042,id_0=13899049652,id_3=13899085531,id_2=13905889105"
        },
        {
            "title": "Outdoor UV Resist Impermeável À Prova D' Água Pvc Estética Adesivo Qr Código Adesivo Logotipo Personalizado Die Cut Vinyl Label Adesivos",
            "description": "Elevate your branding with our Custom UV Resistant Waterproof PVC QR Code Logo Stickers, designed for durability and versatility in both indoor and outdoor environments. These stickers are crafted from high-quality waterproof PVC material that resists fading from UV exposure, making them perfect for long-term use on signage, promotional materials, or product packaging. Each sticker features a die-cut design that ensures a clean, professional look when applied, while the embedded QR code allows for seamless digital engagement—directing users to websites, social media pages, or promotional content. The waterproof and weather-resistant properties of these stickers make them ideal for use on vehicles, billboards, banners, or even as part of event promotions. Available in a range of sizes and customizable with your logo or text, they offer a modern, sleek appearance that blends functionality with visual appeal. Whether you're promoting a business, launching a new product, or creating interactive marketing content, these stickers provide a cost-effective and eye-catching solution. Their easy-to-apply adhesive ensures a secure bond without leaving residue, and their vibrant colors remain sharp even under harsh conditions. Perfect for businesses looking to enhance visibility and customer interaction through innovative, durable, and stylish sticker solutions.",
            "price": "0.8",
            "moq": "200",
            "imgs": [
            "/opt/data/img/ffb2925b-f684-4810-8e40-15b287bb6c31/1749282239948_9589.png",
            "/opt/data/img/ffb2925b-f684-4810-8e40-15b287bb6c31/1749282240828_9949.png",
            "/opt/data/img/ffb2925b-f684-4810-8e40-15b287bb6c31/1749282241805_1320.png",
            "/opt/data/img/ffb2925b-f684-4810-8e40-15b287bb6c31/1749282242107_3965.png",
            "/opt/data/img/ffb2925b-f684-4810-8e40-15b287bb6c31/1749282243485_4645.png",
            "/opt/data/img/ffb2925b-f684-4810-8e40-15b287bb6c31/1749282244219_4672.png"
            ],
            "product_type": "sticker",
            "delivery_time": "7 days",
            "reference_product": "https://www.alibaba.com/product-detail/Outdoor-UV-Resist-Waterproof-Weatherproof-Pvc_1600994418432.html",
            "reference_product_platform": "ali",
            "employee": "1688【丰和金-张姗】",
            "published_shop": "ali_shop2",
            "trace_id": "8551396b-5e26-447d-bd3f-3515801882c1",
            "workflow_name": "ali_to_ali",
            "task_id": "a949d73f-d87c-4816-85f0-4a06e0f154fb",
            "shot_description": "Custom UV Resistant Waterproof PVC QR Code Logo Stickers - Made from durable waterproof PVC material, these stickers resist fading and are suitable for both indoor and outdoor use. They feature a die-cut design with a custom QR code and logo, ideal for branding on signage, promotional materials, or product packaging. Easy to apply and long-lasting, they are perfect for enhancing visibility and digital engagement.",
            "applicable_scenes": "",
            "tags": "custom qr code stickers waterproof vinyl labels uv resistant pvc stickers die cut logo stickers outdoor signage stickers waterproof qr code stickers promotional stickers die cut vinyl labels brand logo stickers durable waterproof stickers",
            "product_name": "Custom UV Resistant Waterproof PVC QR Code Logo Sticker",
            "code": 200,
            "short_description": "",
            "title_mask_count": 0,
            "description_mask_count": 0,
            "short_description_mask_count": 0,
            "str_photos": "id_5=13905901052,id_4=13905853424,url_4=https://sc04.alicdn.com/kf/H321110515ce04c0280ef190addb67ee6U/231139578/H321110515ce04c0280ef190addb67ee6U.png,url_5=https://sc04.alicdn.com/kf/H9ab134feb46f4844a38b853339b3c36eA/231139578/H9ab134feb46f4844a38b853339b3c36eA.png,url_2=https://sc04.alicdn.com/kf/Hfa4fffc851c049bea8c563bf3d63323dX/231139578/Hfa4fffc851c049bea8c563bf3d63323dX.png,url_3=https://sc04.alicdn.com/kf/Hb85334ae787a44009edff87c41e91a98W/231139578/Hb85334ae787a44009edff87c41e91a98W.png,url_0=https://sc04.alicdn.com/kf/Hde59891a2e03463b9ee9b5ea630577fbu/231139578/Hde59891a2e03463b9ee9b5ea630577fbu.png,url_1=https://sc04.alicdn.com/kf/H8e745b0abd684df5a73dd6d9eba6eb3dg/231139578/H8e745b0abd684df5a73dd6d9eba6eb3dg.png,id_1=13905901042,id_0=13899049652,id_3=13899085531,id_2=13905889105"
        }
    ]

    print(res)

    return res


@api.post("/workflow/workflow/template")
async def workflow_template(request: Request, user_info: dict = Depends(verify_token)):
        """Workflow template"""
        # data = await request.json()
        return {
            "delay": 500,
            "steps": [
                {
                    "type": "input",
                    "selector": "input#productTitle",
                    "value": "${product.title}",
                    "description": "填写product title"
                },
                {
                    "type": "input",
                    "selector": ".common-input-wrapper textarea",
                    "value": "${product.tags}",
                    "description": "填写关键词"
                },
                {
                    "type": "click",
                    "selector": "#struct-p-1 input",
                    "value": "",
                    "description": "填写原产地"
                },
                {
                    "type": "wait",
                    "value": 500
                },        
                {
                    "type": "input",
                    "selector": ".next-select-popup-wrap .options-search input",
                    "value": "China",
                    "description": "搜索原产地"
                },
                {
                    "type": "click",
                    "selector": "div[title='China']",
                    "value": "",
                    "description": "选择原产地"
                },
                {
                    "type": "wait",
                    "value": 500
                },
                {
                    "type": "click",
                    "selector": "#struct-p-1-1 input",
                    "value": "",
                    "description": "设置省份"
                },
                {
                    "type": "wait",
                    "value": 500
                },
                {
                    "type": "click",
                    "selector": "div[title='Guangdong']",
                    "value": "",
                    "description": "选择省份"
                },
                {
                    "type": "input",
                    "selector": "#struct-p-371575050 input",
                    "value": "Accept Customized",
                    "description": "设置logo/图文定制工艺"
                },
                {
                    "type": "input",
                    "selector": "#struct-p-2 input",
                    "value": "FH",
                    "description": "设置品牌"

                },
                {
                    "type": "input",
                    "selector": "#struct-p-191284014 input",
                    "value": "Accept Customized",
                    "description": "设置材料"

                },
                {
                    "type": "input",
                    "selector": "#struct-p-3 input",
                    "value": "FH-001",
                    "description": "设置型号"

                },
                {
                    "type": "input",
                    "selector": ".content > div > .next-select .next-select-values input",
                    "value": "Accept Customized",
                    "description": "设置行业应用"

                },
                {
                    "type": "wait",
                    "value": 500
                },
                {
                    "type": "click",
                    "selector": "span.next-menu-item-text:contains('Accept Customized')",
                    "value": "",
                    "description": "设置行业应用"
                },
                {
                    "type": "click",
                    "selector": ".add-attr-btn > span",
                    "description": "点击添加自定义属性"
                },
                {
                    "type": "click",
                    "selector": ".add-attr-btn > span",
                    "description": "点击添加自定义属性"
                },
                {
                    "type": "click",
                    "selector": ".add-attr-btn > span",
                    "description": "点击添加自定义属性"
                },
                {
                    "type": "click",
                    "selector": ".add-attr-btn > span",
                    "description": "点击添加自定义属性"
                },
                {
                    "type": "click",
                    "selector": ".add-attr-btn > span",
                    "description": "点击添加自定义属性"
                },
                {
                    "type": "click",
                    "selector": ".add-attr-btn > span",
                    "description": "点击添加自定义属性"
                },
                {
                    "type": "click",
                    "selector": ".add-attr-btn > span",
                    "description": "点击添加自定义属性"
                },
                {
                    "type": "click",
                    "selector": ".add-attr-btn > span",
                    "description": "点击添加自定义属性"
                },
                {
                    "type": "click",
                    "selector": ".add-attr-btn > span",
                    "description": "点击添加自定义属性"
                },
                {
                    "type": "input",
                    "selector": "input[index='0'][name='text']",
                    "value": "Size",
                    "description": "设置自定义属性名称1"   
                },
                {
                    "type": "input",
                    "selector": "input[index='0'][name='value']",
                    "value": "Accept Customized",
                    "description": "设置自定义属性值1"   
                },
                {
                    "type": "input",
                    "selector": "input[index='1'][name='text']",
                    "value": "Color",
                    "description": "设置自定义属性名称2"   
                },
                {
                    "type": "input",
                    "selector": "input[index='1'][name='value']",
                    "value": "Accept Customized",
                    "description": "设置自定义属性值2"   
                },
                {
                    "type": "input",
                    "selector": "input[index='2'][name='text']",
                    "value": "Shape",
                    "description": "设置自定义属性名称3"   
                },
                {
                    "type": "input",
                    "selector": "input[index='2'][name='value']",
                    "value": "Accept Customized",
                    "description": "设置自定义属性值3"   
                },
                {
                    "type": "input",
                    "selector": "input[index='3'][name='text']",
                    "value": "Feature",
                    "description": "设置自定义属性名称4"   
                },
                {
                    "type": "input",
                    "selector": "input[index='3'][name='value']",
                    "value": "Accept Customized, Waterproof/Oil proof/Writable/Quick Dry/...",
                    "description": "设置自定义属性值4"   
                },
                {
                    "type": "input",
                    "selector": "input[index='4'][name='text']",
                    "value": "Printing",
                    "description": "设置自定义属性名称5"   
                },
                {
                    "type": "input",
                    "selector": "input[index='4'][name='value']",
                    "value": "Accept Customized, Offset/UV/Digital/Color/Laser/...",
                    "description": "设置自定义属性值5"   
                },
                {
                    "type": "input",
                    "selector": "input[index='5'][name='text']",
                    "value": "Packing",
                    "description": "设置自定义属性名称6"   
                },
                {
                    "type": "input",
                    "selector": "input[index='5'][name='value']",
                    "value": "Accept Customized",
                    "description": "设置自定义属性值6"   
                },
                {
                    "type": "input",
                    "selector": "input[index='6'][name='text']",
                    "value": "Logo",
                    "description": "设置自定义属性名称7"   
                },
                {
                    "type": "input",
                    "selector": "input[index='6'][name='value']",
                    "value": "Accept Customized",
                    "description": "设置自定义属性值7"   
                },
                {
                    "type": "input",
                    "selector": "input[index='7'][name='text']",
                    "value": "MOQ",
                    "description": "设置自定义属性名称8"   
                },
                {
                    "type": "input",
                    "selector": "input[index='7'][name='value']",
                    "value": "${product.moq}",
                    "description": "设置自定义属性值8"   
                },
                {
                    "type": "input",
                    "selector": "input[index='8'][name='text']",
                    "value": "Delivery time",
                    "description": "设置自定义属性名称9"   
                },
                {
                    "type": "input",
                    "selector": "input[index='8'][name='value']",
                    "value": "7-20 Days",
                    "description": "设置自定义属性值9"   
                }
            ]
        }
