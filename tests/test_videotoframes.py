import pytest

from videotoframes.video_to_frames import main


def test_main_no_arguments(capsys):
	with pytest.raises(SystemExit) as e:
		main()
	captured = capsys.readouterr()
	assert 'videotoframes: error: the following arguments are required: -o, -i' in captured.err


def test_main_no_output(capsys, tmpdir):
	with pytest.raises(SystemExit) as e:
		main(['-i', './'])
	captured = capsys.readouterr()
	assert 'videotoframes: error: the following arguments are required: -o\n' in captured.err


def test_main_no_input(capsys, tmpdir):
	with pytest.raises(SystemExit) as e:
		main(['-o', './'])
	captured = capsys.readouterr()
	assert 'videotoframes: error: the following arguments are required: -i\n' in captured.err