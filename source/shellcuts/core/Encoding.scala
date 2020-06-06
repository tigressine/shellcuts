package shellcuts.core

import java.nio.charset.Charset
import shellcuts.core.structures.{
  Configuration,
  Shellcut
}

object Encoding {
  val SmallDelimiter = "\0"
  val BigDelimiter = "\0\0\0"
  val GlobalsPattern = """^([^\u0000]*)\0([^\u0000]*)""".r
  val ShellcutPattern =
    """\0\0\0([^\u0000]+)\0([^\u0000]*)((?:\0[^\u0000]+)+)""".r
  val PathPattern = """\0([^\u0000]+)""".r

  // Decode a configuration string into a Configuration object.
  def decode(encoded: String): Configuration = {
    val (crumb, defaultFollow) = GlobalsPattern.findFirstIn(encoded) map {
      case GlobalsPattern(crumb, defaultFollow) => (
        if (crumb.isEmpty) None else Some(crumb),
        if (defaultFollow.isEmpty) None else Some(defaultFollow)
      )
    } getOrElse((None, None))

    val shellcuts = ShellcutPattern.findAllIn(encoded).toList map {
      case ShellcutPattern(name, follow, paths) => {
        Shellcut(
          name,
          if (follow.isEmpty) None else Some(follow),
          PathPattern.findAllIn(paths).toList map {
            case PathPattern(path) => path
          }
        )
      }
    }

    Configuration(crumb, defaultFollow, shellcuts)
  }

  // Encode a Configuration object into a configuration string.
  def encode(charset: Charset)(configuration: Configuration): String = {
    val head = configuration.crumb.getOrElse("") +
      SmallDelimiter +
      configuration.defaultFollow.getOrElse("")

    val body = configuration.shellcuts map {
      (shellcut) => {
        (shellcut.name :: shellcut.follow.getOrElse("") :: shellcut.paths)
          .mkString(SmallDelimiter)
      }
    } mkString(BigDelimiter)

    if (body.isEmpty) {
      head
    } else {
      head + BigDelimiter + body
    }
  }
}
