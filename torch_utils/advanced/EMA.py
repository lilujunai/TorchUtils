class EMA():
    def __init__(self, model, decay):
        self.model = model
        self.decay = decay
        self.shadow = {}
        self.backup = {}

    def register(self):
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                self.shadow[name] = param.data.clone()

    def update(self):
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                assert name in self.shadow
                new_average = (1.0 - self.decay) * param.data + self.decay * self.shadow[name]
                self.shadow[name] = new_average.clone()
    
    def apply_shadow(self):
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                assert name in self.shadow
                self.backup[name] = param.data
                param.data = self.shadow[name]
    
    def restore(self):
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                assert name in self.backup
                param.data = self.backup[name]
        self.backup = {}

'''
# 初始化
ema = EMA(model, 0.999)
ema.register()

# 训练过程中，更新完参数后，同步update shadow weights
def train():
    optimizer.step()
    ema.update()

# eval前，apply shadow weights；eval之后，恢复原来模型的参数
def evaluate():
    ema.apply_shadow()
    # evaluate
    ema.restore()
'''

'''
# pytorch 1.6.0 +
ema_avg = lambda averaged_model_parameter, model_parameter, num_averaged:\
        0.1 * averaged_model_parameter + 0.9 * model_parameter
ema_model = torch.optim.swa_utils.AveragedModel(model, avg_fn=ema_avg)
for i in range(EPOCH):
    xxxx
    if i > ema_start:
        ema_model.update_parameters(model)
torch.optim.swa_utils.update_bn(loader, ema_model)
preds = ema_model(test_input)
'''

# SWA in pytorch 1.6 https://pytorch.org/blog/pytorch-1.6-now-includes-stochastic-weight-averaging/#how-to-use-swa-in-pytorch
# https://github.com/rwightman/pytorch-image-models/blob/master/timm/utils/model_ema.py
