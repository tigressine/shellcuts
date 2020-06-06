package shellcuts.core.operations

import org.scalatest.{
  EitherValues,
  FlatSpec
}
import shellcuts.core.structures.{
  Configuration,
  Shellcut
}

class GoOperationSpec extends FlatSpec with EitherValues {
  "modify()" should "do nothing to an empty configuration" in {
    val givenConfig = Configuration(None, None, List())
    val givenProperties = List("home", "working")
    val givenParameters = List("name")
    val expectedConfig = Configuration(None, None, List())

    val producedConfig = GoOperation.modify(
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
    val givenParameters = List("name")
    val expectedConfig = Configuration(
      None,
      None,
      List(
        Shellcut("name1", None, List("working1")),
        Shellcut("name2", None, List("working2")),
        Shellcut("name3", None, List("working3"))
      )
    )

    val producedConfig = GoOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }

  "command()" should "give an error if no shellcut matches a given name" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name1", None, List("working1")))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name2")
    val expectedMessage = s"""no shellcut named "name2""""

    val producedMessage = GoOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "jump without a follow command" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name1", None, List("working1")))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name1")
    val expectedCommand = s"""cd 'working1'; """

    val producedCommand = GoOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }

  it should "jump with the default follow command when available" in {
    val givenConfig = Configuration(
      None,
      Some("default"),
      List(Shellcut("name1", None, List("working1")))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name1")
    val expectedCommand = s"""cd 'working1'; default"""

    val producedCommand = GoOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }

  it should "jump with the custom follow command when available" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name1", Some("follow1"), List("working1")))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name1")
    val expectedCommand = s"""cd 'working1'; follow1"""

    val producedCommand = GoOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }

  it should "override the default with the custom follow command" in {
    val givenConfig = Configuration(
      None,
      Some("default"),
      List(Shellcut("name1", Some("follow1"), List("working1")))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name1")
    val expectedCommand = s"""cd 'working1'; follow1"""

    val producedCommand = GoOperation.command(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedCommand == producedCommand.right.value)
  }
}
