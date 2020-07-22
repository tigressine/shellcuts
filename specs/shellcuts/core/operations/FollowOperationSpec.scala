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

class FollowOperationSpec extends FlatSpec with EitherValues {
  "modify()" should "handle a missing follow command" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedMessage = "no follow command provided"

    val producedMessage = FollowOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "handle a shellcut that doesn't exist" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List("name", "follow")
    val expectedMessage = """no shellcut with the name "name""""

    val producedMessage = FollowOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "set the default follow command when no shellcut is given" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List("follow")
    val expectedConfig = Configuration(None, Some("follow"), List())

    val producedConfig = FollowOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "set a shellcut-specific follow command" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, "working1"))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name", "follow")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", Some("follow"), "working1"))
    )

    val producedConfig = FollowOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "overwrite an existing shellcut" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", Some("follow1"), "working1"))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name", "follow2")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", Some("follow2"), "working1"))
    )

    val producedConfig = FollowOperation.modify(
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
        Shellcut("name", None, "working1"),
        Shellcut("name", None, "working2"),
        Shellcut("name", None, "working3")
      )
    )
    val givenProperties = List("home", "working4")
    val givenParameters = List("name", "follow")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", Some("follow"), "working1"))
    )

    val producedConfig = FollowOperation.modify(
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
      List(Shellcut("name", None, "working1"))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name", "follow2")
    val expectedConfig = Configuration(
      Some("crumb"),
      Some("follow1"),
      List(Shellcut("name", Some("follow2"), "working1"))
    )

    val producedConfig = FollowOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  "command()" should "show an update message for a default follow" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List("follow")
    val expectedCommand = Command(
      PrintLineAction,
      List("default follow command updated")
    )

    val producedCommand = FollowOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }

  it should "show an update message for a shellcut-specific follow" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", Some("follow"), "working1"))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name", "follow")
    val expectedCommand = Command(
      PrintLineAction,
      List("""follow command updated for shellcut "name"""")
    )

    val producedCommand = FollowOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }
}
