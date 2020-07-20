package shellcuts.core.operations

import org.scalatest.{
  EitherValues,
  FlatSpec
}
import shellcuts.core.actions.PrintLineAction
import shellcuts.core.structures.{
  Command,
  Configuration
}

class CrumbOperationSpec extends FlatSpec with EitherValues {
  "modify()" should "handle missing properties" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List()
    val givenParameters = List()
    val expectedMessage = "working directory could not be determined"

    val producedMessage = CrumbOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "create a crumb in an empty config" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedConfig = Configuration(Some("working"), None, List())

    val producedConfig = CrumbOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "overwrite an old crumb" in {
    val givenConfig = Configuration(Some("working1"), None, List())
    val givenProperties = List("home", "working2")
    val givenParameters = List()
    val expectedConfig = Configuration(Some("working2"), None, List())

    val producedConfig = CrumbOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  "command()" should "show a creation message" in {
    val givenConfig = Configuration(Some("working"), None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedCommand = Command(
      PrintLineAction,
      List("crumb added for this location")
    )

    val producedCommand = CrumbOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }
}
