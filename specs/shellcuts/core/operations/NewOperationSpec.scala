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

class NewOperationSpec extends FlatSpec with EitherValues {
  "modify()" should "handle a missing shellcut name" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedMessage = "no name provided for new shellcut"

    val producedMessage = NewOperation.modify(
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
    val expectedMessage =
      "working directory and/or home directory could not be determined"

    val producedMessage = NewOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "create a shellcut in an empty config" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List("name")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, "working"))
    )

    val producedConfig = NewOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "create a shellcut in a non-empty config" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name1", None, "working1"))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name2")
    val expectedConfig = Configuration(
      None,
      None,
      List(
        Shellcut("name2", None, "working2"),
        Shellcut("name1", None, "working1")
      )
    )

    val producedConfig = NewOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "create a shellcut with a given follow command" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List("name", "follow")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", Some("follow"), "working"))
    )

    val producedConfig = NewOperation.modify(
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
      List(Shellcut("name", None, "working1"))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, "working2"))
    )

    val producedConfig = NewOperation.modify(
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
    val givenParameters = List("name")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, "working4"))
    )

    val producedConfig = NewOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "preserve globals in a config" in {
    val givenConfig = Configuration(Some("crumb"), Some("follow"), List())
    val givenProperties = List("home", "working")
    val givenParameters = List("name")
    val expectedConfig = Configuration(
      Some("crumb"),
      Some("follow"),
      List(Shellcut("name", None, "working"))
    )

    val producedConfig = NewOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  "command()" should "show a creation message with an empty configuration" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List("name")
    val expectedCommand = Command(
      PrintLineAction,
      List("""new shellcut "name" created""")
    )

    val producedCommand = NewOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }

  it should "show a creation message with a populated configuration" in {
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
    val givenParameters = List("name4")
    val expectedCommand = Command(
      PrintLineAction,
      List("""new shellcut "name4" created""")
    )

    val producedCommand = NewOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }
}
