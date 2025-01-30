from bot import Bot
import mcpi.minecraft as minecraft
import mcpi.block as block


class BuilderBot(Bot):
    def __init__(self):
        super().__init__("BuilderBot")

    def on_message(self, mc: minecraft.Minecraft, msg):
        x, y, z = mc.player.getTilePos()

        # Walls
        mc.setBlocks(x - 2, y - 1, z - 2,
                     x + 2, y + 3, z + 2,
                     block.WOOD_PLANKS)
        # Inside
        mc.setBlocks(x - 1, y, z - 1,
                     x + 1, y + 2, z + 1,
                     block.AIR)
        # Door
        mc.setBlock(x - 2, y, z, block.DOOR_WOOD, 0)
        mc.setBlock(x - 2, y + 1, z, block.Block(64, 8))
