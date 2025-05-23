# model settings
norm_cfg = dict(type='SyncBN', requires_grad=True)

data_preprocessor = dict(
    type='DualInputSegDataPreProcessor',
    mean=[123.675, 116.28, 103.53] * 2,
    std=[58.395, 57.12, 57.375] * 2,
    bgr_to_rgb=True,
    size_divisor=32,
    pad_val=0,
    seg_pad_val=255,
    test_cfg=dict(size_divisor=32))

# distillation loss
distill_loss = dict(
    type='DistillLossWithPixel_ChangeStar',
    temperature=2.0,     
    loss_weight=0.0,
    pixel_weight=0.001,
)

model = dict(
    type='DistillSiamEncoderDecoder_ChangeStar',
    distill_loss=distill_loss,  
    data_preprocessor=data_preprocessor,
    pretrained=None,
    backbone=dict(
        type='mmseg.ResNetV1c',
        init_cfg=dict(
            type='Pretrained', 
            checkpoint='open-mmlab://resnet18_v1c'),
        depth=18,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        dilations=(1, 1, 1, 1),
        strides=(1, 2, 2, 2),
        norm_cfg=norm_cfg,
        norm_eval=False,
        style='pytorch',
        contract_dilation=True),
    neck=dict(type='FeatureFusionNeck', policy='concat'),
    decode_head=dict(
        type='ChangeStarHead',
        inference_mode='t1t2',
        in_channels=[1, 1, 1, 1], # useless, placeholder
        in_index=[0, 1, 2, 3],
        channels=96, # same with inner_channels in changemixin_cfg
        num_classes=2,
        out_channels=1,
        threshold=0.5,
        seg_head_cfg=dict(
            type='mmseg.UPerHead',
            in_channels=[64, 128, 256, 512],
            in_index=[0, 1, 2, 3],
            pool_scales=(1, 2, 3, 6),
            channels=128,
            norm_cfg=norm_cfg,
            align_corners=False),
        changemixin_cfg=dict(
            in_channels=128 * 2,
            inner_channels=96, # d_c
            num_convs=1, # N
            ),
        loss_decode=dict(
            type='mmseg.CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0)),
    # model training and testing settings
    train_cfg=dict(),
    test_cfg=dict(mode='whole'))