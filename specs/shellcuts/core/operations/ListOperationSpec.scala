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

class ListOperationSpec extends FlatSpec with EitherValues {
  "modify()" should "do nothing to an empty configuration" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedConfig = Configuration(None, None, List())

    val producedConfig = ListOperation.modify(
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

    val producedConfig = ListOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  "command()" should "handle an empty list of shellcuts" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedMessage = """no shellcuts yet"""

    val producedMessage = ListOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "handle a shellcut that doesn't exist" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name1", None, "working1"))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name2")
    val expectedMessage = """no shellcut with the name "name2""""

    val producedMessage = ListOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "print a shellcut without a follow command" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, "working"))
    )
    val givenProperties = List("home", "working")
    val givenParameters = List("name")
    val expectedCommand = Command(PrintLineAction, List("name   working"))

    val producedCommand = ListOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }

  it should "print a shellcut with a follow command" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", Some("follow"), "working"))
    )
    val givenProperties = List("home", "working")
    val givenParameters = List("name")
    val expectedCommand = Command(
      PrintLineAction,
      List("name   working   follow")
    )

    val producedCommand = ListOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }

  it should "print all shellcuts when no name is provided" in {
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
    val expectedCommand = Command(
      PrintLineAction,
      List(
        "name1   working1",
        "name2   working2",
        "name3   working3"
      )
    )

    val producedCommand = ListOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }

  it should "pad shellcut names to match the longest shellcut name" in {
    val givenConfig = Configuration(
      None,
      None,
      List(
        Shellcut("name1", None, "working1"),
        Shellcut("name20", None, "working20"),
        Shellcut("name3000", None, "working3000")
      )
    )
    val givenProperties = List("home", "working4")
    val givenParameters = List()
    val expectedCommand = Command(
      PrintLineAction,
      List(
        "name1      working1",
        "name20     working20",
        "name3000   working3000"
      )
    )

    val producedCommand = ListOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }
}
