package shellcuts.core.operations

import org.scalatest.{
  EitherValues,
  FlatSpec
}
import shellcuts.core.actions.{
  JumpAction,
  JumpAndFollowAction
}
import shellcuts.core.structures.{
  Command,
  Configuration,
  Shellcut
}

class RetraceOperationSpec extends FlatSpec with EitherValues {
  "modify()" should "do nothing to an empty configuration" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedConfig = Configuration(None, None, List())

    val producedConfig = RetraceOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "do nothing to a populated configuration" in {
    val givenConfig = Configuration(
      Some("working4"),
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
      Some("working4"),
      None,
      List(
        Shellcut("name1", None, List("working1")),
        Shellcut("name2", None, List("working2")),
        Shellcut("name3", None, List("working3"))
      )
    )

    val producedConfig = RetraceOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  "command()" should "give an error if no crumb is available" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedMessage = "no crumb was available"

    val producedMessage = RetraceOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "retrace without the default follow command" in {
    val givenConfig = Configuration(Some("working"), None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedCommand = Command(JumpAction, List("working"))

    val producedCommand = RetraceOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }

  it should "retrace with the default follow command when available" in {
    val givenConfig = Configuration(Some("working"), Some("default"), List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedCommand = Command(
      JumpAndFollowAction,
      List("working", "default")
    )

    val producedCommand = RetraceOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }
}
