from ast import main
import os
import oss2
from typing import Optional

class OSSUploader:
    """阿里云OSS上传工具类"""
    
    def __init__(self, 
                #  access_key_id: str,
                #  access_key_secret: str,
                 endpoint: str,
                 bucket_name: str):
        """
        初始化OSS上传器
        
        Args:
            access_key_id: 阿里云AccessKeyId
            access_key_secret: 阿里云AccessKeySecret
            endpoint: OSS访问域名
            bucket_name: OSS存储空间名称
        """
        access_key_id = os.getenv('OSS_ACCESS_KEY_ID')
        access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET')

        if not access_key_id or not access_key_secret:
            raise ValueError("Access Key ID and Secret must be set as environment variables")
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
        # 保存endpoint和bucket_name用于生成HTTP地址
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        
    def get_file_url(self, oss_file_path: str) -> str:
        """
        根据OSS文件路径生成HTTP访问地址
        
        Args:
            oss_file_path: OSS上的文件路径
            
        Returns:
            str: 文件的HTTP访问地址
        """
        # 处理endpoint格式
        if self.endpoint.startswith('http'):
            # 如果endpoint已包含协议，替换为bucket域名格式
            base_url = self.endpoint.replace('://', f'://{self.bucket_name}.')
        else:
            # 如果endpoint不包含协议，添加https协议和bucket前缀
            base_url = f"https://{self.bucket_name}.{self.endpoint}"
        
        return f"{base_url}/{oss_file_path}"
        
    def upload_file(self,
                    local_file_path: str,
                    oss_file_path: Optional[str] = None,
                    headers: Optional[dict] = None) -> str:
        """
        上传文件到OSS
        
        Args:
            local_file_path: 本地文件路径
            oss_file_path: OSS上的文件路径,默认使用本地文件名
            headers: 上传时的HTTP头部,可选
            
        Returns:
            str: 文件在OSS上的路径
        """
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"本地文件不存在: {local_file_path}")
            
        if oss_file_path is None:
            oss_file_path = os.path.basename(local_file_path)
            
        # 上传文件
        with open(local_file_path, 'rb') as f:
            self.bucket.put_object(oss_file_path, f, headers=headers)
            
        # 返回OSS路径
        return oss_file_path
        
    def upload_file_with_url(self,
                            local_file_path: str,
                            oss_file_path: Optional[str] = None,
                            headers: Optional[dict] = None) -> dict:
        """
        上传文件到OSS并返回路径和HTTP地址
        
        Args:
            local_file_path: 本地文件路径
            oss_file_path: OSS上的文件路径,默认使用本地文件名
            headers: 上传时的HTTP头部,可选
            
        Returns:
            dict: 包含oss_path和http_url的字典
        """
        oss_path = self.upload_file(local_file_path, oss_file_path, headers)
        http_url = self.get_file_url(oss_path)
        
        return {
            "oss_path": oss_path,
            "http_url": http_url
        }
        
    def upload_bytes(self,
                    file_content: bytes,
                    oss_file_path: str,
                    headers: Optional[dict] = None) -> str:
        """
        上传二进制内容到OSS
        
        Args:
            file_content: 文件二进制内容
            oss_file_path: OSS上的文件路径
            headers: 上传时的HTTP头部,可选
            
        Returns:
            str: 文件在OSS上的路径
        """
        self.bucket.put_object(oss_file_path, file_content, headers=headers)
        return oss_file_path
        
    def upload_bytes_with_url(self,
                             file_content: bytes,
                             oss_file_path: str,
                             headers: Optional[dict] = None) -> dict:
        """
        上传二进制内容到OSS并返回路径和HTTP地址
        
        Args:
            file_content: 文件二进制内容
            oss_file_path: OSS上的文件路径
            headers: 上传时的HTTP头部,可选
            
        Returns:
            dict: 包含oss_path和http_url的字典
        """
        oss_path = self.upload_bytes(file_content, oss_file_path, headers)
        http_url = self.get_file_url(oss_path)
        
        return {
            "oss_path": oss_path,
            "http_url": http_url
        }

# 使用示例:
"""
# 创建上传器实例
uploader = OSSUploader(
    access_key_id='your_access_key_id',
    access_key_secret='your_access_key_secret', 
    endpoint='oss-cn-beijing.aliyuncs.com',
    bucket_name='your-bucket-name'
)

# 上传本地文件
url = uploader.upload_file(
    local_file_path='./test.jpg',
    oss_file_path='images/test.jpg'
)

# 上传二进制内容
content = b'Hello World'
url = uploader.upload_bytes(
    file_content=content,
    oss_file_path='test.txt'
)
"""

if __name__ == '__main__':
    # 初始化 OSS 上传器
    uploader = OSSUploader(
        endpoint='https://oss-us-east-1.aliyuncs.com',  # 根据实际情况修改
        bucket_name='tradefree'  # 使用实际的bucket名称
    )
    url = uploader.upload_file_with_url(
        local_file_path='/Users/huahua/Desktop/bbq/lbuicdnn.png',
        oss_file_path='images/test.jpg'
    )
    print(url)
