class ModelService:
    # 原始服务类，包含敏感和非敏感方法
    def predict(self, data):
        return "Prediction result."
    
    def retrain(self, data):
        print("Retraining the model...")
        return "Retraining started."

class ModelServiceProxy:
    # 保护代理
    def __init__(self, original_service, user_role):
        self._service = original_service
        self._user_role = user_role

    def predict(self, data):
        # 无需权限检查
        return self._service.predict(data)

    def retrain(self, data):
        # 需要权限检查
        if self._user_role == 'admin':
            return self._service.retrain(data)
        else:
            raise PermissionError("你没有权限进行模型重训练。")

# 使用代理
admin_proxy = ModelServiceProxy(ModelService(), 'admin')
print(admin_proxy.predict([1, 2, 3]))  # 可以正常访问
print(admin_proxy.retrain([4, 5, 6]))  # 管理员有权限

user_proxy = ModelServiceProxy(ModelService(), 'user')
print(user_proxy.predict([1, 2, 3]))  # 可以正常访问
print(user_proxy.retrain([4, 5, 6])) # 报错：PermissionError