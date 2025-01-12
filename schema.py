import graphene
from models.user import Query as UserQuery, CreateUser, UpdateUser, DeleteUser
from models.transaction import Query as TransactionQuery, CreateTransaction, UpdateTransaction, DeleteTransaction
from models.transaction_type import Query as TransactionTypeQuery, CreateTransactionType, UpdateTransactionType, DeleteTransactionType
from models.clothes import Query as ClothesQuery, CreateClothes, UpdateClothes, DeleteClothes
from models.clothes_type import Query as ClothesTypeQuery, CreateClothesType, UpdateClothesType, DeleteClothesType
from models.exp_mest_clothes import Query as ExpMestClothesQuery, CreateExpMestClothes, UpdateExpMestClothes, DeleteExpMestClothes
from models.imp_mest_clothes import Query as ImpMestClothesQuery, CreateImpMestClothes, UpdateImpMestClothes, DeleteImpMestClothes
from models.imp_mest_type import Query as ImpMestTypeQuery, CreateImpMestType, UpdateImpMestType, DeleteImpMestType
from models.report_type import Query as ReportTypeQuery, CreateReportType, UpdateReportType, DeleteReportType
from models.report_detail import Query as ReportDetailQuery, CreateReportDetail, UpdateReportDetail, DeleteReportDetail
from models.bill import Query as BillQuery, CreateBill, UpdateBill, DeleteBill
from models.plugins import Query as PluginsQuery, CreatePlugin, UpdatePlugin, DeletePlugin

# Kết hợp Query
class Query(
    UserQuery,
    TransactionQuery,
    PluginsQuery,
    TransactionTypeQuery,
    ClothesQuery,
    ClothesTypeQuery,
    ExpMestClothesQuery,
    ImpMestClothesQuery,
    ImpMestTypeQuery,
    ReportTypeQuery,
    ReportDetailQuery,
    BillQuery,
):
    pass

# Kết hợp Mutation
class Mutation(graphene.ObjectType):
    # User Mutations
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    # Plugins Mutations
    create_plugins = CreatePlugin.Field()
    update_plugins = UpdatePlugin.Field()
    delete_plugins = DeletePlugin.Field()
    # Transaction Mutations
    create_transaction = CreateTransaction.Field()
    update_transaction = UpdateTransaction.Field()
    delete_transaction = DeleteTransaction.Field()

    # Transaction Type Mutations
    create_transaction_type = CreateTransactionType.Field()
    update_transaction_type = UpdateTransactionType.Field()
    delete_transaction_type = DeleteTransactionType.Field()

    # Clothes Mutations
    create_clothes = CreateClothes.Field()
    update_clothes = UpdateClothes.Field()
    delete_clothes = DeleteClothes.Field()

    # Clothes Type Mutations
    create_clothes_type = CreateClothesType.Field()
    update_clothes_type = UpdateClothesType.Field()
    delete_clothes_type = DeleteClothesType.Field()

    # Exp Mest Clothes Mutations
    create_exp_mest_clothes = CreateExpMestClothes.Field()
    update_exp_mest_clothes = UpdateExpMestClothes.Field()
    delete_exp_mest_clothes = DeleteExpMestClothes.Field()

    # Imp Mest Clothes Mutations
    create_imp_mest_clothes = CreateImpMestClothes.Field()
    update_imp_mest_clothes = UpdateImpMestClothes.Field()
    delete_imp_mest_clothes = DeleteImpMestClothes.Field()

    # Imp Mest Type Mutations
    create_imp_mest_type = CreateImpMestType.Field()
    update_imp_mest_type = UpdateImpMestType.Field()
    delete_imp_mest_type = DeleteImpMestType.Field()

    # Report Type Mutations
    create_report_type = CreateReportType.Field()
    update_report_type = UpdateReportType.Field()
    delete_report_type = DeleteReportType.Field()

    # Report Detail Mutations
    create_report_detail = CreateReportDetail.Field()
    update_report_detail = UpdateReportDetail.Field()
    delete_report_detail = DeleteReportDetail.Field()

    # Bill Mutations
    create_bill = CreateBill.Field()
    update_bill = UpdateBill.Field()
    delete_bill = DeleteBill.Field()

# Tạo Schema GraphQL
schema = graphene.Schema(query=Query, mutation=Mutation)
