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

class UnfollowOperationSpec extends FlatSpec with EitherValues {
  "modify()" should "handle a shellcut that doesn't exist" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List("name")
    val expectedMessage = """no shellcut with the name "name""""

    val producedMessage = UnfollowOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "remove the default follow command when no shellcut is given" in {
    val givenConfig = Configuration(None, Some("follow"), List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedConfig = Configuration(None, None, List())

    val producedConfig = UnfollowOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "remove a shellcut-specific follow command" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", Some("follow"), List("working1")))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, List("working1")))
    )

    val producedConfig = UnfollowOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "overwrite multiple existing shellcuts" in {
    val givenConfig = Configuration(
      None,
      None,
      List(
        Shellcut("name", Some("follow1"), List("working1")),
        Shellcut("name", Some("follow2"), List("working2")),
        Shellcut("name", Some("follow3"), List("working3"))
      )
    )
    val givenProperties = List("home", "working4")
    val givenParameters = List("name")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, List("working1")))
    )

    val producedConfig = UnfollowOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "preserve globals in a config" in {
    val givenConfig = Configuration(
      Some("crumb"),
      Some("follow1"),
      List(Shellcut("name", Some("follow2"), List("working1")))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name")
    val expectedConfig = Configuration(
      Some("crumb"),
      Some("follow1"),
      List(Shellcut("name", None, List("working1")))
    )

    val producedConfig = UnfollowOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  "command()" should "show a removal message for a default follow" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedCommand = Command(
      PrintLineAction,
      List("default follow command removed")
    )

    val producedCommand = UnfollowOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }

  it should "show a removal message for a shellcut-specific follow" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, List("working1")))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name")
    val expectedCommand = Command(
      PrintLineAction,
      List("""follow command removed for shellcut "name"""")
    )

    val producedCommand = UnfollowOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }
}
