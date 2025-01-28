from bot import Bot

import mcpi
import mcpi.block

class BuilderBot(Bot):
    def __init__(self):
        super().__init__("BuilderBot")
        
    def on_message(self, mc: mcpi.minecraft.Minecraft, msg):
        x, y, z = mc.player.getTilePos()

        # Walls
        mc.setBlocks(x-2, y-1, z-2,
                     x+2, y+3, z+2,
                     mcpi.block.WOOD_PLANKS)
        # Inside
        mc.setBlocks(x-1, y-0, z-1,
                     x+1, y+2, z+1,
                     mcpi.block.AIR)
        # Door
        mc.setBlock(x-2, y, z, mcpi.block.DOOR_WOOD, 0)
        mc.setBlock(x-2, y+1, z, mcpi.block.Block(64, 8))