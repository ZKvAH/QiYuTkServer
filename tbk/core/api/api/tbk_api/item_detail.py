from typing import Optional

from fastapi import Body, Depends
from pydantic import Field
from qiyu_api.dtk_api import DtkStdApi
from qiyu_api.tbk_api import ItemInfo
from structlog.stdlib import BoundLogger

from core.forms.tbk import TbkItemDetailForm
from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_std
from ...api.app import app
from ...api_utils import api_inner_wrapper


class TbkGoodsDetailResponseModel(ResponseModel):
    data: Optional[ItemInfo] = Field(None, title="详细数据")


@app.post(
    "/tbk/item_detail",
    tags=["淘宝客"],
    summary="单品详情",
    response_model=TbkGoodsDetailResponseModel,
)
async def tbk_item_detail(
    args: TbkItemDetailForm = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
    tbk: DtkStdApi = Depends(get_dtk_std),
):
    """
    获取淘宝客的单品详情
    """

    @api_inner_wrapper(logger)
    async def inner():
        j = await tbk.get_goods_detail(args.tao_id)
        if j is None:
            return ApiResp.from_errno(AppErrno.tbk_error)
        return ApiResp.from_data(j)

    return await inner
