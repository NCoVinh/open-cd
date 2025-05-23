crop_size = (
    512,
    512,
)
data_preprocessor = dict(
    bgr_to_rgb=True,
    mean=[
        123.675,
        116.28,
        103.53,
        123.675,
        116.28,
        103.53,
    ],
    pad_val=0,
    seg_pad_val=255,
    size_divisor=32,
    std=[
        58.395,
        57.12,
        57.375,
        58.395,
        57.12,
        57.375,
    ],
    test_cfg=dict(size_divisor=32),
    type='DualInputSegDataPreProcessor')
data_root = '/home/share/remote_sense/S2Looking/'
dataset_type = 'S2Looking_Dataset'
default_hooks = dict(
    checkpoint=dict(
        by_epoch=False, interval=8000, save_best='mIoU',
        type='CheckpointHook'),
    logger=dict(interval=1000, log_metric_by_epoch=False, type='LoggerHook'),
    param_scheduler=dict(type='ParamSchedulerHook'),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    timer=dict(type='IterTimerHook'),
    visualization=dict(
        img_shape=(
            1024,
            1024,
            3,
        ), interval=1, type='CDVisualizationHook'))
default_scope = 'opencd'
env_cfg = dict(
    cudnn_benchmark=True,
    dist_cfg=dict(backend='nccl'),
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0))
img_ratios = [
    0.75,
    1.0,
    1.25,
]
launcher = 'none'
load_from = None
log_level = 'INFO'
log_processor = dict(by_epoch=False)
model = dict(
    backbone=dict(
        depths=[
            2,
            2,
            4,
            2,
        ],
        drop_path_rate=0.2,
        drop_rate=0.0,
        embed_dims=[
            64,
            128,
            320,
            512,
        ],
        init_cfg=dict(
            checkpoint=
            '/home/u1120230285/lyx/data/pretrained/lsk_s_backbone.pth.tar',
            type='Pretrained'),
        interaction_cfg=(
            None,
            dict(p=0.5, type='SpatialExchange'),
            dict(p=0.5, type='ChannelExchange'),
            dict(p=0.5, type='ChannelExchange'),
        ),
        norm_cfg=dict(requires_grad=True, type='SyncBN'),
        type='LSKNet'),
    data_preprocessor=dict(
        bgr_to_rgb=True,
        mean=[
            123.675,
            116.28,
            103.53,
            123.675,
            116.28,
            103.53,
        ],
        pad_val=0,
        seg_pad_val=255,
        size_divisor=32,
        std=[
            58.395,
            57.12,
            57.375,
            58.395,
            57.12,
            57.375,
        ],
        test_cfg=dict(size_divisor=32),
        type='DualInputSegDataPreProcessor'),
    decode_head=dict(
        align_corners=False,
        channels=128,
        dropout_ratio=0.1,
        in_channels=[
            64,
            128,
            320,
            512,
        ],
        in_index=[
            0,
            1,
            2,
            3,
        ],
        loss_decode=dict(
            loss_weight=1.0, type='mmseg.CrossEntropyLoss', use_sigmoid=False),
        norm_cfg=dict(requires_grad=True, type='SyncBN'),
        num_classes=2,
        sampler=dict(
            min_kept=100000, thresh=0.7, type='mmseg.OHEMPixelSampler'),
        type='Changer'),
    pretrained=None,
    test_cfg=dict(mode='whole'),
    train_cfg=dict(),
    type='DIEncoderDecoder')
norm_cfg = dict(requires_grad=True, type='SyncBN')
optim_wrapper = dict(
    optimizer=dict(
        betas=(
            0.9,
            0.999,
        ), lr=0.0002, type='AdamW', weight_decay=0.01),
    type='OptimWrapper')
optimizer = dict(
    betas=(
        0.9,
        0.999,
    ), lr=0.0002, type='AdamW', weight_decay=0.01)
param_scheduler = [
    dict(
        begin=0, by_epoch=False, end=1000, start_factor=1e-06,
        type='LinearLR'),
    dict(
        begin=1000,
        by_epoch=False,
        end=80000,
        eta_min=0.0,
        power=1.0,
        type='PolyLR'),
]
resume = False
test_cfg = dict(type='TestLoop')
test_dataloader = dict(
    batch_size=1,
    dataset=dict(
        data_prefix=dict(
            img_path_from='test/Image1',
            img_path_to='test/Image2',
            seg_map_path='test/label'),
        data_root='/home/share/remote_sense/S2Looking/',
        pipeline=[
            dict(type='MultiImgLoadImageFromFile'),
            dict(keep_ratio=True, scale=(
                1024,
                1024,
            ), type='MultiImgResize'),
            dict(type='MultiImgLoadAnnotations'),
            dict(type='MultiImgPackSegInputs'),
        ],
        type='S2Looking_Dataset'),
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler'))
test_evaluator = dict(
    iou_metrics=[
        'mFscore',
        'mIoU',
    ], type='mmseg.IoUMetric')
test_pipeline = [
    dict(type='MultiImgLoadImageFromFile'),
    dict(keep_ratio=True, scale=(
        1024,
        1024,
    ), type='MultiImgResize'),
    dict(type='MultiImgLoadAnnotations'),
    dict(type='MultiImgPackSegInputs'),
]
train_cfg = dict(max_iters=80000, type='IterBasedTrainLoop', val_interval=8000)
train_dataloader = dict(
    batch_size=8,
    dataset=dict(
        data_prefix=dict(
            img_path_from='train/Image1',
            img_path_to='train/Image2',
            seg_map_path='train/label'),
        data_root='/home/share/remote_sense/S2Looking/',
        pipeline=[
            dict(type='MultiImgLoadImageFromFile'),
            dict(type='MultiImgLoadAnnotations'),
            dict(
                degree=(
                    -20,
                    20,
                ),
                flip_prob=0.5,
                rotate_prob=0.5,
                type='MultiImgRandomRotFlip'),
            dict(
                cat_max_ratio=0.75,
                crop_size=(
                    512,
                    512,
                ),
                type='MultiImgRandomCrop'),
            dict(prob=0.5, type='MultiImgExchangeTime'),
            dict(
                brightness_delta=10,
                contrast_range=(
                    0.8,
                    1.2,
                ),
                hue_delta=10,
                saturation_range=(
                    0.8,
                    1.2,
                ),
                type='MultiImgPhotoMetricDistortion'),
            dict(type='MultiImgPackSegInputs'),
        ],
        type='S2Looking_Dataset'),
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=True, type='InfiniteSampler'))
train_pipeline = [
    dict(type='MultiImgLoadImageFromFile'),
    dict(type='MultiImgLoadAnnotations'),
    dict(
        degree=(
            -20,
            20,
        ),
        flip_prob=0.5,
        rotate_prob=0.5,
        type='MultiImgRandomRotFlip'),
    dict(
        cat_max_ratio=0.75, crop_size=(
            512,
            512,
        ), type='MultiImgRandomCrop'),
    dict(prob=0.5, type='MultiImgExchangeTime'),
    dict(
        brightness_delta=10,
        contrast_range=(
            0.8,
            1.2,
        ),
        hue_delta=10,
        saturation_range=(
            0.8,
            1.2,
        ),
        type='MultiImgPhotoMetricDistortion'),
    dict(type='MultiImgPackSegInputs'),
]
tta_model = dict(type='mmseg.SegTTAModel')
tta_pipeline = [
    dict(backend_args=None, type='MultiImgLoadImageFromFile'),
    dict(
        transforms=[
            [
                dict(
                    keep_ratio=True, scale_factor=0.75, type='MultiImgResize'),
                dict(keep_ratio=True, scale_factor=1.0, type='MultiImgResize'),
                dict(
                    keep_ratio=True, scale_factor=1.25, type='MultiImgResize'),
            ],
            [
                dict(
                    direction='horizontal',
                    prob=0.0,
                    type='MultiImgRandomFlip'),
                dict(
                    direction='horizontal',
                    prob=1.0,
                    type='MultiImgRandomFlip'),
            ],
            [
                dict(type='MultiImgLoadAnnotations'),
            ],
            [
                dict(type='MultiImgPackSegInputs'),
            ],
        ],
        type='TestTimeAug'),
]
val_cfg = dict(type='ValLoop')
val_dataloader = dict(
    batch_size=1,
    dataset=dict(
        data_prefix=dict(
            img_path_from='test/Image1',
            img_path_to='test/Image2',
            seg_map_path='test/label'),
        data_root='/home/share/remote_sense/S2Looking/',
        pipeline=[
            dict(type='MultiImgLoadImageFromFile'),
            dict(keep_ratio=True, scale=(
                1024,
                1024,
            ), type='MultiImgResize'),
            dict(type='MultiImgLoadAnnotations'),
            dict(type='MultiImgPackSegInputs'),
        ],
        type='S2Looking_Dataset'),
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler'))
val_evaluator = dict(
    iou_metrics=[
        'mFscore',
        'mIoU',
    ], type='mmseg.IoUMetric')
vis_backends = [
    dict(type='CDLocalVisBackend'),
]
visualizer = dict(
    alpha=1.0,
    name='visualizer',
    type='CDLocalVisualizer',
    vis_backends=[
        dict(type='CDLocalVisBackend'),
    ])
work_dir = './work_dirs/changer_ex_lsk_s_512x512_80k_s2looking'
