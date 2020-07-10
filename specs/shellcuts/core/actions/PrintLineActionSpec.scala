package shellcuts.core.actions

import org.scalatest.{
  EitherValues,
  FlatSpec
}

class PrintLineActionSpec extends FlatSpec with EitherValues {
  "posixFormat()" should "handle an empty argument list" in {
    val givenArguments = List()
    val expectedMessage = "could not format command, no argument provided"

    val producedMessage = PrintLineAction.posixFormat(givenArguments)
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "handle a single argument" in {
    val givenArguments = List("argument")
    val expectedString = raw"printf '%s\n' 'argument'"

    val producedString = PrintLineAction.posixFormat(givenArguments)
    assert(expectedString == producedString.right.value)
  }

  it should "handle multiple arguments" in {
    val givenArguments = List("argument1", "argument2", "argument3")
    val expectedString = raw"printf '%s\n' 'argument1' 'argument2' 'argument3'"

    val producedString = PrintLineAction.posixFormat(givenArguments)
    assert(expectedString == producedString.right.value)
  }

  it should "handle an argument with an apostrophe" in {
    val givenArguments = List("argu'ment")
    val expectedString = raw"printf '%s\n' 'argu'\''ment'"

    val producedString = PrintLineAction.posixFormat(givenArguments)
    assert(expectedString == producedString.right.value)
  }
}
