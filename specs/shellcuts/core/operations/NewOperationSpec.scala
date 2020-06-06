package shellcuts.core.operations

import org.scalatest.{
  EitherValues,
  FlatSpec
}
import shellcuts.core.structures.{
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
      List(Shellcut("name", None, List("working")))
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
      List(Shellcut("name1", None, List("working1")))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name2")
    val expectedConfig = Configuration(
      None,
      None,
      List(
        Shellcut("name2", None, List("working2")),
        Shellcut("name1", None, List("working1"))
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
      List(Shellcut("name", Some("follow"), List("working")))
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
      List(Shellcut("name", None, List("working1")))
    )
    val givenProperties = List("home", "working2")
    val givenParameters = List("name")
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, List("working2")))
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
      List(Shellcut("name", None, List("working")))
    )

    val producedConfig = NewOperation.modify(
      givenConfig,
      givenProperties,
      givenParameters
    )
    assert(expectedConfig == producedConfig.right.value)
  }
}
