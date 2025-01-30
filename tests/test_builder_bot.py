import unittest
from unittest.mock import patch, MagicMock
from builderbot import BuilderBot
import mcpi.block as block


class TestBuilderBot(unittest.TestCase):

    @patch("mcpi.minecraft.Minecraft")          # Simulate Minecraft connexion
    def test_on_message_builds_house(self, mock_minecraft):
        # Simulate Minecraft instance
        mock_mc = MagicMock()
        mock_minecraft.return_value = mock_mc

        # Simulate player pos
        mock_mc.player.getTilePos.return_value = (10, 5, 15)

        # Create BuilderBot instance
        bot = BuilderBot()

        # Simulate message for bot
        bot.on_message(mock_mc, "build")

        # Expected values for building
        x, y, z = 10, 5, 15
        expected_walls_call = (x - 2, y - 1, z - 2, x + 2, y + 3, z + 2, block.WOOD_PLANKS)
        expected_inside_call = (x - 1, y, z - 1, x + 1, y + 2, z + 1, block.AIR)
        expected_door_calls = [
            (x - 2, y, z, block.DOOR_WOOD, 0),
            (x - 2, y + 1, z, block.Block(64, 8))
        ]

        # Validate expected call to setBlocks for walls
        mock_mc.setBlocks.assert_any_call(*expected_walls_call)

        # Validate expected call to setBlocks for inside
        mock_mc.setBlocks.assert_any_call(*expected_inside_call)

        # Validate expected call to setBlocks for door
        for call in expected_door_calls:
            mock_mc.setBlock.assert_any_call(*call)


if __name__ == "__main__":
    unittest.main()