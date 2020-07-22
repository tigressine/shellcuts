package shellcuts.core.operations

import org.scalatest.{
  EitherValues,
  FlatSpec
}
import shellcuts.core.actions.PrintLineAction
import shellcuts.core.structures.{
  Command,
  Configuration,
  Shellcut
}

class VersionOperationSpec extends FlatSpec with EitherValues {
  "modify()" should "do nothing to an empty configuration" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedConfig = Configuration(None, None, List())

    val producedConfig = VersionOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "do nothing to a populated configuration" in {
    val givenConfig = Configuration(
      None,
      None,
      List(
        Shellcut("name1", None, "working1"),
        Shellcut("name2", None, "working2"),
        Shellcut("name3", None, "working3")
      )
    )
    val givenProperties = List("home", "working4")
    val givenParameters = List()
    val expectedConfig = Configuration(
      None,
      None,
      List(
        Shellcut("name1", None, "working1"),
        Shellcut("name2", None, "working2"),
        Shellcut("name3", None, "working3")
      )
    )

    val producedConfig = VersionOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  "command()" should "produce a version prompt" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()

    val producedCommand = VersionOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(PrintLineAction == producedCommand.right.value.action)
    assert(!producedCommand.right.value.arguments.isEmpty)
    assert(!producedCommand.right.value.arguments(0).isEmpty)
  }
}
