from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from ai.dao.entity.employee import Employee
from ai.dao.entity.employee_access import EmployeeAccess
from ai.dao.entity.user import User
from ai.dao.db.engine import manager_engine
from ai.service.employee_catch_service import EmployeeCacheService
from datetime import datetime

class EmployeeService:
    def __init__(self):
        self.session = Session(bind=manager_engine)
        self.cache_service = EmployeeCacheService()

    def refresh_employee_access_catch(self, employee_id: str) -> bool:
        """通过employee_id获取员工信息并更新缓存
        
        Args:
            employee_id: 员工ID
            
        Returns:
            bool: 更新缓存是否成功
        """
        try:
            # 查询员工信息
            employee = self.session.query(Employee).filter(
                Employee.id == employee_id,
                Employee.is_enable == True
            ).first()
            
            if not employee:
                return False
                
            # 查询用户信息以获取user_group
            user = self.session.query(User).filter(
                User.username == employee.user_name,
                User.is_enable == True
            ).first()
            
            if not user:
                return False
                
            # 查询员工的访问权限
            accesses = self.session.query(EmployeeAccess).filter(
                EmployeeAccess.employee_id == employee.id,
                EmployeeAccess.is_enable == True
            ).all()

            employee_accesses = []
            for access in accesses:
                employee_accesses.append(access.to_dict())
            temp = EmployeeAccess()
            temp.user_id = user.id
            temp.employee_id = employee.id
            temp.workflow = "verify_to_verify"
            temp.workflow_name = "关键词有效性验证"
            temp.src_platform = "verify"
            temp.dest_platform = "verify"
            temp.product_type = "verify"
            temp.shop_id = 10000000
            temp.shop_name = "关键词验证"
            temp.category_id = 10000000
            temp.template_id = 10000000
            temp.is_enable = True
            temp.created_at = datetime.now()
            temp.updated_at = datetime.now()

            employee_accesses.append(temp.to_dict())
            
            # 查询相关的发品模板
            # templates = {}
            # for access in accesses:
            #     template = self.session.query(access.template_id).first()
            #     if template:
            #         templates[access.template_id] = template
            
            # 构建返回数据
            result = {
                "employee_token": employee.employee_token,
                "user_info": {
                    "user_id": user.id,
                    "user_name": user.username,
                    "user_cn_name": user.user_cn_name,
                    "user_company": user.company,
                    "user_group": user.user_group
                },
                "employee_info": {
                    "employee_id": employee.id,
                    "employee_name": employee.employee_name,
                    "employee_cn_name": employee.employee_cn_name,
                    "employee_token": employee.employee_token
                },
                "employee_accesses": employee_accesses,
                # "templates": templates
            }
            
            # 将数据存入缓存
            self.cache_service.set_to_cache(employee.employee_token, result)
            
            return True
            
        except Exception as e:
            print(f"Error getting employee by id: {str(e)}")
            return False
        finally:
            self.session.close()

    def refresh_employee_accesses_catch(self) -> int:
        """刷新所有员工的访问权限缓存
        
        Returns:
            int: 成功更新缓存的员工数量
        """
        try:
            # 清空所有员工缓存信息
            self.cache_service.clear_all_cache()
            
            # 查询所有启用的员工
            employees = self.session.query(Employee).filter(
                Employee.is_enable == True
            ).all()
            
            if not employees:
                return 0
                
            success_count = 0
            for employee in employees:
                # 使用 refresh_employee_access_catch 方法更新每个员工的缓存
                if self.refresh_employee_access_catch(str(employee.id)):
                    success_count += 1
            
            return success_count
            
        except Exception as e:
            print(f"Error refreshing employee accesses cache: {str(e)}")
            return 0
        finally:
            self.session.close()

    def __del__(self):
        """确保session被正确关闭"""
        if hasattr(self, 'session'):
            self.session.close() 