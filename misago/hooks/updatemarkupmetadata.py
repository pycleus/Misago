from ..types import GraphQLContext, ParsedMarkupMetadata, UpdateMarkupMetadataAction
from .action import ActionHook


class UpdateMarkupMetadataHook(ActionHook[UpdateMarkupMetadataAction]):
    async def call_action(
        self, context: GraphQLContext, ast: dict, metadata: ParsedMarkupMetadata
    ):
        return await self.gather(context, ast, metadata)