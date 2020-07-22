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

class DeleteOperationSpec extends FlatSpec with EitherValues {
  "modify()" should "handle a missing shellcut name" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List()
    val expectedMessage = "no name provided for deletion"

    val producedMessage = DeleteOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "handle a config with no shellcuts" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List("name")
    val expectedConfig = Configuration(None, None, List())

    val producedConfig = DeleteOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "handle a config without the target shellcut" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name1", None, "path1"))
    )
    val givenProperties = List("home", "working")
    val givenParameters = List("name2")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name1", None, "path1"))
    )

    val producedConfig = DeleteOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "remove a target shellcut from a config" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, "path"))
    )
    val givenProperties = List("home", "working")
    val givenParameters = List("name")
    val expectedConfig = Configuration(None, None, List())

    val producedConfig = DeleteOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  it should "remove duplicate target shellcuts from a config" in {
    val givenConfig = Configuration(
      None,
      None,
      List(
        Shellcut("name1", None, "path1"),
        Shellcut("name2", None, "path2"),
        Shellcut("name3", None, "path3"),
        Shellcut("name1", None, "path1"),
        Shellcut("name4", None, "path4")
      )
    )
    val givenProperties = List("home", "working")
    val givenParameters = List("name1")
    val expectedConfig = Configuration(
      None,
      None,
      List(
        Shellcut("name2", None, "path2"),
        Shellcut("name3", None, "path3"),
        Shellcut("name4", None, "path4")
      )
    )

    val producedConfig = DeleteOperation.modify(
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
    val expectedConfig = Configuration(Some("crumb"), Some("follow"), List())

    val producedConfig = DeleteOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  "command()" should "show a deletion message with an empty configuration" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List("name")
    val expectedCommand = Command(
      PrintLineAction,
      List("""shellcut "name" deleted""")
    )

    val producedCommand = DeleteOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }

  it should "show a deletion message with a populated configuration" in {
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
    val givenParameters = List("name1")
    val expectedCommand = Command(
      PrintLineAction,
      List("""shellcut "name1" deleted""")
    )

    val producedCommand = DeleteOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }
}
