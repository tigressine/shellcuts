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

class MoveOperationSpec extends FlatSpec with EitherValues {
  "modify()" should "handle a missing shellcut name" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedMessage = "no shellcut name provided"

    val producedMessage = MoveOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "handle missing properties" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List()
    val givenParameters = List("name")
    val expectedMessage = "working directory could not be determined"

    val producedMessage = MoveOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "handle a shellcut that doesn't exist" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List("name")
    val expectedMessage = """no shellcut with the name "name""""

    val producedMessage = MoveOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "move an existing shellcut" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, List("working1")))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, List("working2")))
    )

    val producedConfig = MoveOperation.modify(
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
        Shellcut("name", None, List("working1")),
        Shellcut("name", None, List("working2")),
        Shellcut("name", None, List("working3"))
      )
    )
    val givenProperties = List("home", "working4")
    val givenParameters = List("name")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, List("working4")))
    )

    val producedConfig = MoveOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "preserve globals and shellcut-specific metadata" in {
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
      List(Shellcut("name", Some("follow2"), List("working2")))
    )

    val producedConfig = MoveOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  "command()" should "show a move message" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, List("working")))
    )
    val givenProperties = List("home", "working")
    val givenParameters = List("name")
    val expectedCommand = Command(
      PrintLineAction,
      List("""shellcut "name" moved""")
    )

    val producedCommand = MoveOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }
}
