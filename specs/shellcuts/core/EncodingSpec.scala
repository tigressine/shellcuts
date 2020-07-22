package shellcuts.core

import java.nio.charset.StandardCharsets
import org.scalatest.FlatSpec
import shellcuts.core.structures.{
  Configuration,
  Shellcut
}

class EncodingSpec extends FlatSpec {
  val encode = Encoding.encode(StandardCharsets.UTF_8) _

  "decode()" should "handle an empty string" in {
    val encodedConfig = ""
    val expectedConfig = Configuration(None, None, List())

    assert(expectedConfig == Encoding.decode(encodedConfig))
  }

  it should "handle a malformed string" in {
    val encodedConfig = "malformed"
    val expectedConfig = Configuration(None, None, List())

    assert(expectedConfig == Encoding.decode(encodedConfig))
  }

  it should "handle a string with a nameless shellcut" in {
    val encodedConfig = "\0\0\0\0\0\0path"
    val expectedConfig = Configuration(None, None, List())

    assert(expectedConfig == Encoding.decode(encodedConfig))
  }

  it should "process a string with one shellcut" in {
    val encodedConfig = "\0\0\0\0name\0\0path"
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, "path"))
    )

    assert(expectedConfig == Encoding.decode(encodedConfig))
  }

  it should "process a string with one shellcut that has a follow command" in {
    val encodedConfig = "\0\0\0\0name\0follow\0path"
    val expectedConfig = Configuration(
      None,
      None,
      List(Shellcut("name", Some("follow"), "path"))
    )

    assert(expectedConfig == Encoding.decode(encodedConfig))
  }

  it should "process a string that contains Unicode" in {
    val encodedConfig = "crumb😀\0follow😀\0\0\0name😀\0follow😀\0path😀"
    val expectedConfig = Configuration(
      Some("crumb😀"),
      Some("follow😀"),
      List(Shellcut("name😀", Some("follow😀"), "path😀"))
    )

    assert(expectedConfig == Encoding.decode(encodedConfig))
  }

  it should "process a string with one global" in {
    val encodedConfig = "\0follow"
    val expectedConfig = Configuration(None, Some("follow"), List())

    assert(expectedConfig == Encoding.decode(encodedConfig))
  }

  it should "process a string with both globals" in {
    val encodedConfig = "crumb\0follow"
    val expectedConfig = Configuration(Some("crumb"), Some("follow"), List())

    assert(expectedConfig == Encoding.decode(encodedConfig))
  }

  it should "process a string with both globals and one shellcut" in {
    val encodedConfig = "crumb\0follow\0\0\0name\0\0path"
    val expectedConfig = Configuration(
      Some("crumb"),
      Some("follow"),
      List(Shellcut("name", None, "path"))
    )

    assert(expectedConfig == Encoding.decode(encodedConfig))
  }

  it should "process a string with both globals and multiple shellcuts" in {
    val encodedConfig = "crumb\0follow" +
      "\0\0\0name1\0\0path1" +
      "\0\0\0name2\0\0path2" +
      "\0\0\0name3\0\0path3"
    val expectedConfig = Configuration(
      Some("crumb"),
      Some("follow"),
      List(
        Shellcut("name1", None, "path1"),
        Shellcut("name2", None, "path2"),
        Shellcut("name3", None, "path3")
      )
    )

    assert(expectedConfig == Encoding.decode(encodedConfig))
  }

  "encode()" should "handle an empty config" in {
    val givenConfig = Configuration(None, None, List())
    val encodedConfig = "\0"

    assert(encodedConfig == encode(givenConfig))
  }

  it should "process a config with one shellcut" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", None, "path"))
    )
    val encodedConfig = "\0\0\0\0name\0\0path"

    assert(encodedConfig == encode(givenConfig))
  }

  it should "process a config with one shellcut that has a follow command" in {
    val givenConfig = Configuration(
      None,
      None,
      List(Shellcut("name", Some("follow"), "path"))
    )
    val encodedConfig = "\0\0\0\0name\0follow\0path"

    assert(encodedConfig == encode(givenConfig))
  }

  it should "process a config that contains Unicode" in {
    val givenConfig = Configuration(
      Some("crumb😀"),
      Some("follow😀"),
      List(Shellcut("name😀", Some("follow😀"), "path😀"))
    )
    val encodedConfig = "crumb😀\0follow😀\0\0\0name😀\0follow😀\0path😀"

    assert(encodedConfig == encode(givenConfig))
  }

  it should "process a config with one global" in {
    val givenConfig = Configuration(None, Some("follow"), List())
    val encodedConfig = "\0follow"

    assert(encodedConfig == encode(givenConfig))
  }

  it should "process a config with both globals" in {
    val givenConfig = Configuration(Some("crumb"), Some("follow"), List())
    val encodedConfig = "crumb\0follow"

    assert(encodedConfig == encode(givenConfig))
  }

  it should "process a config with both globals and one shellcut" in {
    val givenConfig = Configuration(
      Some("crumb"),
      Some("follow"),
      List(Shellcut("name", None, "path"))
    )
    val encodedConfig = "crumb\0follow\0\0\0name\0\0path"

    assert(encodedConfig == encode(givenConfig))
  }

  it should "process a config with both globals and multiple shellcuts" in {
    val givenConfig = Configuration(
      Some("crumb"),
      Some("follow"),
      List(
        Shellcut("name1", None, "path1"),
        Shellcut("name2", None, "path2"),
        Shellcut("name3", None, "path3")
      )
    )
    val encodedConfig = "crumb\0follow" +
      "\0\0\0name1\0\0path1" +
      "\0\0\0name2\0\0path2" +
      "\0\0\0name3\0\0path3"

    assert(encodedConfig == encode(givenConfig))
  }
}
