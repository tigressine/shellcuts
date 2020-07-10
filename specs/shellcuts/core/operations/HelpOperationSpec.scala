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

class HelpOperationSpec extends FlatSpec with EitherValues {
  "modify()" should "do nothing to an empty configuration" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedConfig = Configuration(None, None, List())

    val producedConfig = HelpOperation.modify(
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
        Shellcut("name1", None, List("working1")),
        Shellcut("name2", None, List("working2")),
        Shellcut("name3", None, List("working3"))
      )
    )
    val givenProperties = List("home", "working4")
    val givenParameters = List()
    val expectedConfig = Configuration(
      None,
      None,
      List(
        Shellcut("name1", None, List("working1")),
        Shellcut("name2", None, List("working2")),
        Shellcut("name3", None, List("working3"))
      )
    )

    val producedConfig = HelpOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  "command()" should "produce a printable help prompt" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, List("working1")))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List()

    val producedCommand = HelpOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(PrintLineAction == producedCommand.right.value.action)
    assert(!producedCommand.right.value.arguments.isEmpty)
    assert(!producedCommand.right.value.arguments(0).isEmpty)
  }
}
